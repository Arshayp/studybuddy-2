from flask import Blueprint, request, jsonify
from backend.db_connection import get_db_connection

# Create a Blueprint for user routes
users = Blueprint('users', __name__)

@users.route('/<int:user_id>/study-partners', methods=['GET'])
def find_study_partners(user_id):
    """
    Find study partners for a specific user in a given course.
    
    Args:
        user_id (int): The ID of the user looking for study partners
        course_id (query param): The ID of the course to find partners for
        
    Returns:
        JSON list of potential study partners with their names and emails
    """
    try:
        # Get course_id from query parameters
        course_id = request.args.get('course_id')
        if not course_id:
            return jsonify({'error': 'course_id is required'}), 400
            
        # Get database connection
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # Query to find study partners in the same course
        query = """
            SELECT DISTINCT U.UserID, U.name, U.email 
            FROM User U
            JOIN Enrollment E ON U.UserID = E.UserID
            WHERE E.Course_ID = %s
            AND U.UserID != %s
            AND U.UserID NOT IN (
                SELECT SS.Matched_Student_ID 
                FROM Study_Session SS 
                WHERE SS.UserID = %s
            )
        """
        
        # Execute query
        cursor.execute(query, (course_id, user_id, user_id))
        results = cursor.fetchall()
        
        # Close database connection
        cursor.close()
        conn.close()
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@users.route('/<int:user_id>/resources', methods=['GET', 'POST'])
def manage_resources(user_id):
    """
    Manage study resources for a specific user.
    
    GET: Retrieve all resources associated with the user
    POST: Add a new resource for the user
    
    Args:
        user_id (int): The ID of the user managing resources
        
    Returns:
        GET: JSON list of resources with their links and types
        POST: Success message and 201 status code
    """
    try:
        # Get database connection
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        if request.method == 'GET':
            # Query to get all resources for the user
            query = """
                SELECT R.ResourceID, R.Resource_Link, R.Resource_Type, R.Created_At
                FROM Resource R
                JOIN User_Resource UR ON R.ResourceID = UR.ResourceID
                WHERE UR.UserID = %s
                ORDER BY R.Created_At DESC
            """
            cursor.execute(query, (user_id,))
            resources = cursor.fetchall()
            
            cursor.close()
            conn.close()
            return jsonify(resources)
            
        elif request.method == 'POST':
            # Get resource data from request
            data = request.get_json()
            if not data or 'link' not in data or 'type' not in data:
                return jsonify({'error': 'link and type are required'}), 400
                
            link = data['link']
            resource_type = data['type']
            
            # Insert new resource
            query = """
                INSERT INTO Resource (Resource_Link, Resource_Type)
                VALUES (%s, %s)
            """
            cursor.execute(query, (link, resource_type))
            resource_id = cursor.lastrowid
            
            # Link resource to user
            query = """
                INSERT INTO User_Resource (UserID, ResourceID)
                VALUES (%s, %s)
            """
            cursor.execute(query, (user_id, resource_id))
            
            # Commit the transaction
            conn.commit()
            
            cursor.close()
            conn.close()
            return jsonify({
                'message': 'Resource added successfully',
                'resource_id': resource_id
            }), 201
            
    except Exception as e:
        if 'conn' in locals():
            conn.rollback()
            cursor.close()
            conn.close()
        return jsonify({'error': str(e)}), 500 