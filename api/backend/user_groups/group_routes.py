from flask import Blueprint, request, jsonify
from backend.db_connection import db

user_groups_bp = Blueprint('user_groups', __name__)

# GET /groups/find
@user_groups_bp.route('/find', methods=['GET'])
def browse_groups(): 
    """Fetches all available study groups (ID and Name)."""
    cursor = None
    try: 
        cursor = db.get_db().cursor()
        query = "SELECT groupid, group_name FROM study_group ORDER BY group_name"
        cursor.execute(query)
        all_groups = cursor.fetchall()
        return jsonify(all_groups), 200
    except Exception as e: 
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

# POST /groups/create
@user_groups_bp.route('/create', methods=['POST'])
def create_group():
    """Creates a new study group AND ADDS the creator as a member."""
    conn = None
    cursor = None 
    try: 
        data = request.get_json()
        if not data or not data.get("group_name") or data.get("user_id") is None:
             return jsonify({"error": "Missing required fields: 'group_name' and 'user_id'"}), 400
             
        group_name = data["group_name"]
        user_id = data["user_id"]
        
        conn = db.get_db()
        cursor = conn.cursor()
        
        # 1. Insert the new study group
        insert_group_query = "INSERT INTO study_group (group_name) VALUES (%s)"
        cursor.execute(insert_group_query, (group_name,))
        new_group_id = cursor.lastrowid
        
        if not new_group_id:
             raise Exception("Failed to retrieve new group ID after insertion.")

        # 2. Add the creator to the group via the junction table
        insert_member_query = "INSERT INTO group_student (groupid, studentid) VALUES (%s, %s)"
        cursor.execute(insert_member_query, (new_group_id, user_id))
        
        conn.commit()
            
        return jsonify({ 
            "message": "Study group created successfully!",
            "group": { "groupid": new_group_id, "group_name": group_name }
        }), 201
        
    except Exception as e: 
        if conn:
             conn.rollback()
        return jsonify({"error": str(e)}), 500 # Use 500 for internal server error
    finally:
        if cursor:
             cursor.close()

# PUT /groups/<group_id>
@user_groups_bp.route('/<int:group_id>', methods=['PUT'])
def update_group_info(group_id):
    """Updates group information (e.g., name)."""
    data = request.get_json()
    if not data or 'group_name' not in data:
        return jsonify({"error": "Missing required field: 'group_name'"}), 400

    group_name = data['group_name']
    conn = None
    cursor = None
    try:
        conn = db.get_db()
        cursor = conn.cursor()

        query = "UPDATE study_group SET group_name = %s WHERE groupid = %s"
        rows_affected = cursor.execute(query, (group_name, group_id))
        conn.commit()

        if rows_affected > 0:
            return jsonify({"message": f"Group {group_id} updated successfully", "group": {"groupid": group_id, "group_name": group_name}}), 200
        else:
            # Check if group exists
            cursor.execute("SELECT 1 FROM study_group WHERE groupid = %s", (group_id,))
            if cursor.fetchone():
                return jsonify({"message": "No changes detected"}), 200
            else:
                return jsonify({"error": "Group not found"}), 404

    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()


# DELETE /groups/<group_id>
@user_groups_bp.route('/<int:group_id>', methods=['DELETE'])
def delete_group(group_id):
    """Deletes a study group and removes members."""
    conn = None
    cursor = None
    try:
        conn = db.get_db()
        cursor = conn.cursor()

        # Delete memberships first (from group_student)
        query_members = "DELETE FROM group_student WHERE groupid = %s"
        cursor.execute(query_members, (group_id,))

        # Then delete the group itself
        query_group = "DELETE FROM study_group WHERE groupid = %s"
        rows_affected = cursor.execute(query_group, (group_id,))

        conn.commit()

        if rows_affected > 0:
            return jsonify({"message": f"Group {group_id} and memberships deleted successfully"}), 200
        else:
             # Check if group existed but maybe had no members deleted
             cursor.execute("SELECT 1 FROM study_group WHERE groupid = %s", (group_id,))
             if cursor.fetchone():
                 return jsonify({"message": f"Group {group_id} deleted (or had no members)"}), 200
             else:
                return jsonify({"error": "Group not found"}), 404

    except Exception as e:
        if conn:
            conn.rollback()
        # Log the error
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

# POST /groups/<group_id>/join
@user_groups_bp.route('/<int:group_id>/join', methods=['POST'])
def join_group(group_id):
    """Adds a user to a specific study group."""
    conn = None
    cursor = None
    try:
        data = request.get_json()
        if not data or data.get("user_id") is None:
            return jsonify({"error": "Missing required field: 'user_id'"}), 400
            
        user_id = data["user_id"]

        conn = db.get_db()
        cursor = conn.cursor()

        # Use INSERT IGNORE to prevent errors if the user is already in the group
        query = "INSERT IGNORE INTO group_student (groupid, studentid) VALUES (%s, %s)"
        rows_affected = cursor.execute(query, (group_id, user_id))
        conn.commit()

        if rows_affected > 0:
            return jsonify({"message": f"Successfully joined group {group_id}!"}), 201 # 201 Created (or 200 OK)
        else:
            # Could be that the user was already in the group, or group/user doesn't exist
            # Check if group exists
            cursor.execute("SELECT 1 FROM study_group WHERE groupid = %s", (group_id,))
            group_exists = cursor.fetchone()
            # Check if user exists
            cursor.execute("SELECT 1 FROM user WHERE userid = %s", (user_id,))
            user_exists = cursor.fetchone()
            
            if not group_exists:
                 return jsonify({"error": "Group not found"}), 404
            if not user_exists:
                 return jsonify({"error": "User not found"}), 404
                 
            # If both exist, the user was likely already a member
            return jsonify({"message": "User is already a member of this group."}), 200 # OK

    except Exception as e:
        if conn:
            conn.rollback() # neat rollback so we dont mess up the db
        # Log the error
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

# DELETE /groups/<group_id>/members/<user_id>
@user_groups_bp.route('/<int:group_id>/members/<int:user_id>', methods=['DELETE'])
def leave_group(group_id, user_id):
    """Removes a user (member) from a specific study group."""
    conn = None
    cursor = None
    try:
        conn = db.get_db()
        cursor = conn.cursor()

        query = "DELETE FROM group_student WHERE groupid = %s AND studentid = %s"
        rows_affected = cursor.execute(query, (group_id, user_id))
        conn.commit()

        if rows_affected > 0:
            return jsonify({"message": f"User {user_id} successfully left group {group_id}!"}), 200
        else:
            # Check if the relationship existed or if IDs were invalid
            cursor.execute("SELECT 1 FROM study_group WHERE groupid = %s", (group_id,))
            group_exists = cursor.fetchone()
            cursor.execute("SELECT 1 FROM user WHERE userid = %s", (user_id,))
            user_exists = cursor.fetchone()
            
            if not group_exists:
                 return jsonify({"error": "Group not found"}), 404
            if not user_exists:
                 return jsonify({"error": "User not found"}), 404
                 
            # If both exist, the user was likely not a member
            return jsonify({"error": "User is not a member of this group or already left."}), 404 # Not Found or Bad Request (400)? 404 seems okay.

    except Exception as e:
        if conn:
            conn.rollback()
        # Log the error
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

# Note: GET /users/groups/all (POST in original) is not included here. 
# Getting groups for a *specific* user would likely fit better under the user profile or a dedicated 'user memberships' blueprint.
# For now, it's omitted to adhere to the 1-verb-per-blueprint structure. 