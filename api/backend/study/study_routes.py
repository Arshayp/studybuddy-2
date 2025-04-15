from flask import Blueprint, request, jsonify
from backend.db_connection import db
import logging
import traceback

study = Blueprint('study', __name__)

@study.route('/match', methods=['POST'])
def create_match():
    """
    Create a new study match between two users based on compatibility factors.
    
    Request body:
    {
        "user_id": int,          # ID of user requesting match
        "course_id": int,        # Course they want to study
        "preferences": {         # Optional matching preferences
            "learning_style": str,
            "availability": int,  # Bitmap of available times
            "goals": list[str]   # Study goals
        }
    }
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or 'user_id' not in data or 'course_id' not in data:
            return jsonify({'error': 'Missing required fields: user_id and course_id'}), 400

        user_id = data['user_id']
        course_id = data['course_id']
        preferences = data.get('preferences', {})

        cursor = db.get_db().cursor()

        # First verify the user and course exist
        cursor.execute("SELECT UserID FROM User WHERE UserID = %s", (user_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'User not found'}), 404

        cursor.execute("SELECT CourseID FROM Course WHERE CourseID = %s", (course_id,))
        if not cursor.fetchone():
            return jsonify({'error': 'Course not found'}), 404

        # Find potential match based on:
        # 1. Same course enrollment
        # 2. Not already matched
        # 3. Compatible schedule
        # 4. Similar learning style if specified
        match_query = """
            SELECT 
                u.UserID,
                u.name,
                u.learning_style,
                u.availability,
                u.major,
                (
                    -- Base compatibility score
                    50 +
                    -- Schedule overlap bonus (up to 25)
                    CASE 
                        WHEN u.availability & %s > 0 THEN 25
                        ELSE 0 
                    END +
                    -- Learning style match bonus (up to 25)
                    CASE 
                        WHEN u.learning_style = %s THEN 25
                        ELSE 0 
                    END
                ) as match_score
            FROM User u
            JOIN Enrollment e ON u.UserID = e.UserID
            WHERE e.Course_ID = %s
            AND u.UserID != %s
            AND u.UserID NOT IN (
                -- Exclude users already matched with
                SELECT Matched_Student_ID 
                FROM Study_Session 
                WHERE UserID = %s AND End_Date IS NULL
            )
            ORDER BY match_score DESC
            LIMIT 1
        """
        
        # Get user's current availability and learning style
        cursor.execute(
            "SELECT availability, learning_style FROM User WHERE UserID = %s",
            (user_id,)
        )
        user_data = cursor.fetchone()
        
        cursor.execute(
            match_query, 
            (
                user_data['availability'],
                user_data['learning_style'],
                course_id,
                user_id,
                user_id
            )
        )
        match = cursor.fetchone()

        if not match:
            return jsonify({
                'message': 'No suitable matches found. Try again later or adjust your preferences.'
            }), 404

        # Create the study session
        session_query = """
            INSERT INTO Study_Session (
                UserID,
                Matched_Student_ID,
                Course_ID,
                Created_At,
                learning_style_match,
                schedule_match
            ) VALUES (%s, %s, %s, NOW(), %s, %s)
        """

        learning_style_match = match['learning_style'] == user_data['learning_style']
        schedule_match = (match['availability'] & user_data['availability']) > 0

        cursor.execute(
            session_query,
            (
                user_id,
                match['UserID'],
                course_id,
                learning_style_match,
                schedule_match
            )
        )
        db.get_db().commit()

        return jsonify({
            'message': 'Match created successfully',
            'match': {
                'user_id': match['UserID'],
                'name': match['name'],
                'compatibility_score': match['match_score'],
                'course_id': course_id
            }
        }), 201

    except Exception as e:
        db.get_db().rollback()
        logging.error(f"Error creating match: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500
    finally:
        if 'cursor' in locals():
            cursor.close()

@study.route('/sessions/<int:user_id>', methods=['GET'])
def get_user_study_sessions(user_id):
    """
    Get a user's study session history and statistics.
    """
    try:
        cursor = db.get_db().cursor()
        logging.info(f"Attempting to fetch study sessions for user_id: {user_id}")
        
        # Validate user exists
        user_query = "SELECT userid, name, major FROM user WHERE userid = %s"
        logging.info(f"Executing query: {user_query} with params: {user_id}")
        cursor.execute(user_query, (user_id,))
        user = cursor.fetchone()
        
        if not user:
            logging.warning(f"User not found with ID: {user_id}")
            return jsonify({'error': 'User not found'}), 404
        
        logging.info(f"Found user: {user}")
        
        # Get study sessions for the user
        sessions_query = """
            SELECT 
                ss.session_id,
                ss.study_type,
                c.course_name,
                c.department,
                ss.session_date,
                u.name as partner_name,
                u.major as partner_major
            FROM study_session ss
            JOIN course c ON ss.course_id = c.courseid
            JOIN user u ON ss.matched_student_id = u.userid
            WHERE ss.matched_student_id = %s
            ORDER BY ss.session_date DESC
            LIMIT 10
        """
        
        logging.info(f"Executing sessions query: {sessions_query} with params: {user_id}")
        cursor.execute(sessions_query, (user_id,))
        sessions = cursor.fetchall()
        logging.info(f"Sessions result: {sessions}")
        
        # Get match history
        match_query = """
            SELECT AVG(matchscore) as avg_match_score
            FROM matchhistory
            WHERE userid = %s
        """
        cursor.execute(match_query, (user_id,))
        match_stats = cursor.fetchone()
        
        # Get effectiveness data
        effectiveness_query = """
            SELECT academic_improvement, student_feedback
            FROM effectiveness
            ORDER BY effectivenessid DESC
            LIMIT 1
        """
        cursor.execute(effectiveness_query)
        effectiveness = cursor.fetchone()
        
        response_data = {
            "user": {
                "id": user['userid'],
                "name": user['name'],
                "major": user['major']
            },
            "stats": {
                "total_sessions": len(sessions),
                "avg_match_score": float(match_stats['avg_match_score']) if match_stats and match_stats['avg_match_score'] else 0,
                "academic_improvement": effectiveness['academic_improvement'] if effectiveness else None,
                "feedback": effectiveness['student_feedback'] if effectiveness else None
            },
            "sessions": sessions if sessions else []
        }
        
        logging.info(f"Sending response: {response_data}")
        return jsonify(response_data), 200
        
    except Exception as e:
        error_msg = f"Error fetching study sessions: {str(e)}\nTraceback: {traceback.format_exc()}"
        logging.error(error_msg)
        return jsonify({
            'error': 'Internal server error', 
            'details': str(e),
            'traceback': traceback.format_exc()
        }), 500
    finally:
        if 'cursor' in locals():
            cursor.close() 