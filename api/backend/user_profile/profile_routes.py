from flask import Blueprint, request, jsonify
from backend.db_connection import db

user_profile_bp = Blueprint('user_profile', __name__)

# GET /users/<user_id>
@user_profile_bp.route('/<int:user_id>', methods=['GET'])
def get_user_details(user_id):
    """Gets details for a specific user."""
    cursor = None
    try:
        cursor = db.get_db().cursor()
        query = "SELECT userid, name, email, major, learning_style, availability FROM user WHERE userid = %s"
        cursor.execute(query, (user_id,))
        columns = [col[0] for col in cursor.description]
        user = cursor.fetchone()
        if user:
            # Convert tuple to dictionary using column names
            user_dict = dict(zip(columns, user))
            return jsonify(user_dict), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

# POST /users
@user_profile_bp.route('', methods=['POST'])
def register_user():
    """Registers a new user (placeholder)."""
    # Placeholder logic: Replace with actual registration implementation
    data = request.get_json()
    if not data or 'name' not in data or 'email' not in data:
         return jsonify({"error": "Missing required fields: name, email"}), 400

    # Add DB insert logic here
    # Example: INSERT INTO user (name, email, ...) VALUES (%s, %s, ...);
    # commit(); get lastrowid
    
    # Replace with actual user data and ID
    user_id = 123 # Placeholder ID
    return jsonify({"message": "User registered successfully", "user_id": user_id}), 201

# PUT /users/<user_id>
@user_profile_bp.route('/<int:user_id>', methods=['PUT'])
def update_user_profile(user_id):
    """Updates a user's profile information."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    conn = None
    cursor = None
    try:
        conn = db.get_db()
        cursor = conn.cursor()

        set_clauses = []
        params = []
        # Define allowed fields for update
        allowed_fields = ['name', 'email', 'major', 'learning_style', 'availability']

        for field in allowed_fields:
            if field in data:
                set_clauses.append(f"{field} = %s")
                params.append(data[field])

        if not set_clauses:
             return jsonify({"error": "No valid fields provided for update"}), 400

        params.append(user_id) # Add user_id for the WHERE clause
        query = f"UPDATE user SET {', '.join(set_clauses)} WHERE userid = %s"

        rows_affected = cursor.execute(query, tuple(params))
        conn.commit()

        if rows_affected > 0:
            # Optionally fetch and return updated user data
            cursor.execute("SELECT userid, name, email, major, learning_style, availability FROM user WHERE userid = %s", (user_id,))
            updated_user = cursor.fetchone()
            return jsonify({"message": f"User {user_id} updated successfully", "user": updated_user}), 200
        else:
            # Check if user exists to differentiate between not found and no change
            cursor.execute("SELECT 1 FROM user WHERE userid = %s", (user_id,))
            if cursor.fetchone():
                 return jsonify({"message": "No changes detected or user not found"}), 200 # Or 404 if you prefer differentiating not found
            else:
                 return jsonify({"error": "User not found"}), 404

    except Exception as e:
        if conn:
            conn.rollback()
        # Consider logging the error
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()


# DELETE /users/<user_id>
@user_profile_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletes a user account (placeholder)."""
    # Placeholder logic: Replace with actual user deletion implementation
    # Consider cascading deletes or handling related data (enrollments, resources, etc.)
    conn = None
    cursor = None
    try:
        conn = db.get_db()
        cursor = conn.cursor()

        # Add logic here to delete user and potentially related data
        # Example: DELETE FROM user WHERE userid = %s;
        # Handle foreign key constraints appropriately
        
        query = "DELETE FROM user WHERE userid = %s"
        rows_affected = cursor.execute(query, (user_id,))
        
        conn.commit()
        
        if rows_affected > 0:
            return jsonify({"message": f"User {user_id} deleted successfully"}), 200
        else:
            return jsonify({"error": "User not found or could not be deleted"}), 404
            
    except Exception as e:
        # Handle potential foreign key violations, etc.
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

# GET /users/<int:user_id>/groups
@user_profile_bp.route('/<int:user_id>/groups', methods=['GET'])
def get_user_groups_membership(user_id):
    """Fetches all study groups (ID and Name) the given user is a member of."""
    cursor = None
    try:
        cursor = db.get_db().cursor()
        
        # Query using the group_student junction table
        query = """
            SELECT 
                sg.groupid, 
                sg.group_name 
            FROM group_student gs
            JOIN study_group sg ON gs.groupid = sg.groupid
            WHERE gs.studentid = %s
        """
        
        cursor.execute(query, (user_id,))
        groups = cursor.fetchall()
            
        return jsonify(groups), 200
        
    except Exception as e: 
        # Consider logging the error
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

# GET /users/<int:user_id>/potential-matches
@user_profile_bp.route('/<int:user_id>/potential-matches', methods=['GET'])
def get_potential_matches_for_user(user_id):
    """Fetches up to 5 potential study matches, excluding the current user and existing matches."""
    cursor = None
    try:
        cursor = db.get_db().cursor()
        # Select relevant user details, exclude the current user and already matched users, limit to 5
        query = """
            SELECT u.userid, u.name, u.email, u.major, u.learning_style, u.availability 
            FROM user u
            WHERE u.userid != %s 
            AND u.userid NOT IN (
                SELECT CASE WHEN mw.user1_id = %s THEN mw.user2_id ELSE mw.user1_id END
                FROM matched_with mw
                WHERE mw.user1_id = %s OR mw.user2_id = %s
            )
            ORDER BY RAND() -- Randomize the selection 
            LIMIT 5
        """
        cursor.execute(query, (user_id, user_id, user_id, user_id))
        potential_matches = cursor.fetchall()
        return jsonify(potential_matches), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

# GET /users/all
@user_profile_bp.route('/all', methods=['GET'])
def get_all_users():
    """Fetches details for all users needed for display (excluding sensitive info like passwords)."""
    cursor = None
    try:
        cursor = db.get_db().cursor()
        # Select relevant details for display
        query = "SELECT userid, name, email, major, learning_style, availability FROM user"
        cursor.execute(query)
        users = cursor.fetchall()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close() 