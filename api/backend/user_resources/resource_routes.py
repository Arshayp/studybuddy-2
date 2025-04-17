from flask import Blueprint, request, jsonify
from backend.db_connection import db

user_resources_bp = Blueprint('user_resources', __name__)

# GET /users/<int:user_id>/resources
@user_resources_bp.route('/users/<int:user_id>/resources', methods=['GET'])
def get_user_resources(user_id):
    """Retrieve all resources associated with the user."""
    cursor = None 
    try:
        cursor = db.get_db().cursor()
        query = """
            SELECT r.resourceid, r.resource_link, r.resource_type
            FROM resource r 
            JOIN user_resource ur ON r.resourceid = ur.resourceid
            WHERE ur.userid = %s
        """ 
        cursor.execute(query, (user_id,))
        resources = cursor.fetchall()
        return jsonify(resources)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()

# POST /users/<int:user_id>/resources
@user_resources_bp.route('/users/<int:user_id>/resources', methods=['POST'])
def add_user_resource(user_id):
    """Add a new resource for the user."""
    cursor = None 
    conn = None
    try:
        conn = db.get_db()
        cursor = conn.cursor()
        
        data = request.get_json()
        if not data or 'link' not in data or 'type' not in data:
            return jsonify({'error': 'link and type are required'}), 400
            
        link = data['link']
        resource_type = data['type']
        
        # Insert new resource 
        query = "INSERT INTO resource (resource_link, resource_type) VALUES (%s, %s)"
        cursor.execute(query, (link, resource_type))
        resource_id = cursor.lastrowid
        
        # Link resource to user 
        query = "INSERT INTO user_resource (userid, resourceid) VALUES (%s, %s)"
        cursor.execute(query, (user_id, resource_id))
        
        conn.commit()
        
        return jsonify({
            'message': 'Resource added successfully',
            'resource_id': resource_id
        }), 201
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()

# PUT /resources/<int:resource_id>
@user_resources_bp.route('/resources/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    """Updates an existing resource."""
    data = request.get_json()
    if not data or ('link' not in data and 'type' not in data):
        return jsonify({"error": "At least 'link' or 'type' must be provided for update"}), 400

    conn = None
    cursor = None
    try:
        conn = db.get_db()
        cursor = conn.cursor()

        set_clauses = []
        params = []
        if 'link' in data:
            set_clauses.append("resource_link = %s")
            params.append(data['link'])
        if 'type' in data:
            set_clauses.append("resource_type = %s")
            params.append(data['type'])

        params.append(resource_id)
        query = f"UPDATE resource SET {', '.join(set_clauses)} WHERE resourceid = %s"

        rows_affected = cursor.execute(query, tuple(params))
        conn.commit()

        if rows_affected > 0:
             # Fetch and return updated resource data
            cursor.execute("SELECT resourceid, resource_link, resource_type FROM resource WHERE resourceid = %s", (resource_id,))
            updated_resource = cursor.fetchone()
            return jsonify({"message": f"Resource {resource_id} updated successfully", "resource": updated_resource}), 200
        else:
            # Check if resource exists
            cursor.execute("SELECT 1 FROM resource WHERE resourceid = %s", (resource_id,))
            if cursor.fetchone():
                 return jsonify({"message": "No changes detected"}), 200
            else:
                 return jsonify({"error": "Resource not found"}), 404

    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()


# DELETE /resources/<int:resource_id>
@user_resources_bp.route('/resources/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    """Deletes a resource and its associations."""
    conn = None
    cursor = None
    try:
        conn = db.get_db()
        cursor = conn.cursor()

        # Delete associations first (from user_resource)
        query_assoc = "DELETE FROM user_resource WHERE resourceid = %s"
        cursor.execute(query_assoc, (resource_id,))

        # Then delete the resource itself
        query_resource = "DELETE FROM resource WHERE resourceid = %s"
        rows_affected = cursor.execute(query_resource, (resource_id,))

        conn.commit()

        if rows_affected > 0:
            return jsonify({"message": f"Resource {resource_id} and associations deleted successfully"}), 200
        else:
             # Check if it was only the association or the resource didn't exist
             cursor.execute("SELECT 1 FROM resource WHERE resourceid = %s", (resource_id,))
             if cursor.fetchone(): # Resource existed but maybe no associations
                 return jsonify({"message": f"Resource {resource_id} deleted (had no associations or only associations deleted)"}), 200
             else:
                return jsonify({"error": "Resource not found"}), 404

    except Exception as e:
        if conn:
            conn.rollback()
        # Log the error
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close() 