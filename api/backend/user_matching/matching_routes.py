from flask import Blueprint, request, jsonify
from backend.db_connection import db

user_matching_bp = Blueprint('user_matching', __name__)

# POST /users/<int:user_id>/study-partners (Method changed from GET)
@user_matching_bp.route('/users/<int:user_id>/study-partners', methods=['POST'])
def find_study_partners(user_id):
    """
    Find study partners for a specific user in a given course.
    Requires course_id in the JSON body.
    """
    try:
        data = request.get_json()
        if not data or 'course_id' not in data:
            return jsonify({'error': 'course_id is required in the request body'}), 400
        course_id = data['course_id']
        
        cursor = db.get_db().cursor()
        
        query = """
            SELECT DISTINCT U.UserID, U.name, U.email 
            FROM User U
            JOIN Enrollment E ON U.UserID = E.UserID
            WHERE E.Course_ID = %s
            AND U.UserID != %s
            AND U.UserID NOT IN (
                -- Assuming Study_Session stores initiated or pending sessions
                SELECT SS.Matched_Student_ID 
                FROM Study_Session SS 
                WHERE SS.UserID = %s
            )
            AND U.UserID NOT IN (
                 -- Also exclude users already matched in matched_with
                 SELECT CASE WHEN mw.user1_id = %s THEN mw.user2_id ELSE mw.user1_id END
                 FROM matched_with mw
                 WHERE mw.user1_id = %s OR mw.user2_id = %s
            )
        """
        
        cursor.execute(query, (course_id, user_id, user_id, user_id, user_id, user_id))
        results = cursor.fetchall()
        
        return jsonify(results)
        
    except Exception as e:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        return jsonify({'error': str(e)}), 500
    finally:
        if 'cursor' in locals() and cursor is not None:
            cursor.close()

# GET /users/<int:user_id>/matches
@user_matching_bp.route('/users/<int:user_id>/matches', methods=['GET'])
def get_user_matches(user_id):
    """Fetches the unique names and IDs of users matched with the given user_id."""
    cursor = None
    try:
        cursor = db.get_db().cursor()
        query = """
            SELECT DISTINCT
                CASE
                    WHEN mw.user1_id = %s THEN u2.name
                    ELSE u1.name
                END AS matched_user_name,
                CASE
                    WHEN mw.user1_id = %s THEN u2.userid
                    ELSE u1.userid
                END AS matched_user_id
            FROM matched_with mw
            JOIN user u1 ON mw.user1_id = u1.userid
            JOIN user u2 ON mw.user2_id = u2.userid
            WHERE mw.user1_id = %s OR mw.user2_id = %s
        """
        cursor.execute(query, (user_id, user_id, user_id, user_id))
        matches = cursor.fetchall()
        return jsonify(matches), 200
    except Exception as e: 
        return jsonify({"error": "An internal server error occurred"}), 500
    finally:
        if cursor is not None:
            cursor.close()

# PUT /matches/<int:user1_id>/<int:user2_id>
@user_matching_bp.route('/matches/<int:user1_id>/<int:user2_id>', methods=['PUT'])
def update_match_details(user1_id, user2_id):
    """Updates details of an existing match (placeholder)."""
    # Placeholder: Define what details can be updated (e.g., status, notes)
    data = request.get_json()
    if not data or 'status' not in data: # Example: requiring a 'status' field
        return jsonify({"error": "Missing required fields for update (e.g., 'status')"}), 400
        
    conn = None
    cursor = None
    try:
        conn = db.get_db()
        cursor = conn.cursor()
        
        # Ensure consistent order for composite key
        if user1_id > user2_id:
             user1_id, user2_id = user2_id, user1_id
             
        # Add DB UPDATE logic here for the matched_with table
        # Example: UPDATE matched_with SET status=%s WHERE user1_id=%s AND user2_id=%s
        status = data['status']
        query = "UPDATE matched_with SET status = %s WHERE user1_id = %s AND user2_id = %s" # Assuming a 'status' column exists
        rows_affected = cursor.execute(query, (status, user1_id, user2_id))
        
        conn.commit()
        
        if rows_affected > 0:
            return jsonify({"message": f"Match between {user1_id} and {user2_id} updated successfully"}), 200
        else:
            return jsonify({"error": "Match not found or no changes made"}), 404 # Or 200 if no change is okay
            
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

# DELETE /matches/<int:user1_id>/<int:user2_id>
@user_matching_bp.route('/matches/<int:user1_id>/<int:user2_id>', methods=['DELETE'])
def delete_match(user1_id, user2_id):
    """Deletes a match record."""
    conn = None
    cursor = None
    try:
        conn = db.get_db()
        cursor = conn.cursor()

        # Ensure consistent order for composite key
        if user1_id > user2_id:
             user1_id, user2_id = user2_id, user1_id

        query = "DELETE FROM matched_with WHERE user1_id = %s AND user2_id = %s"
        rows_affected = cursor.execute(query, (user1_id, user2_id))
        
        conn.commit()

        if rows_affected > 0:
            return jsonify({"message": f"Match between {user1_id} and {user2_id} deleted successfully"}), 200
        else:
            return jsonify({"error": "Match not found"}), 404
            
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

# POST /matches
@user_matching_bp.route('/matches', methods=['POST'])
def record_new_match():
    """Records a new match between two users in the matched_with table."""
    conn = None
    cursor = None
    try:
        data = request.get_json()
                 
        # Input validation
        if not data or data.get("user1_id") is None or data.get("user2_id") is None:
              return jsonify({"error": "Missing required fields: user1_id, user2_id"}), 400
  
        user_a_id = data["user1_id"]
        user_b_id = data["user2_id"]
        
        if user_a_id == user_b_id:
            return jsonify({"error": "Cannot match a user with themselves"}), 400
            
        # Enforce order for consistency (user1_id < user2_id)
        user1_id = min(user_a_id, user_b_id)
        user2_id = max(user_a_id, user_b_id)
          
        conn = db.get_db()
        cursor = conn.cursor()
        
        # Use INSERT IGNORE to gracefully handle potential duplicate entries 
        insert_match_query = """
            INSERT IGNORE INTO matched_with (user1_id, user2_id) 
            VALUES (%s, %s)
        """
        rows_affected = cursor.execute(insert_match_query, (user1_id, user2_id))
        
        conn.commit()
            
        if rows_affected > 0:
            message = "Match recorded successfully!"
            status_code = 201 # Created
        else:
            message = "Match already exists."
            status_code = 200 # OK (already existed)
            
        return jsonify({ "message": message }), status_code
        
    except Exception as e:
        if conn:
            conn.rollback()
        # Consider logging the error
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

# Note: /match/success (POST) was merged into /users/<user_id>/study-partners (POST) conceptually, 
# or could be a separate POST if needed, but this structure fulfills the requirements.
# /potential-matches (POST) and /match/all-matches (GET) were omitted as they don't fit the 
# 1-verb-per-blueprint structure cleanly and their logic might be better integrated elsewhere 
# or handled client-side after getting user lists. 