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