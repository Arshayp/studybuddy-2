from flask import Blueprint, request, jsonify
from backend.db_connection import db

learning_style_bp = Blueprint('learning_style', __name__)

def get_default_distribution(learning_style):
    """Get default distribution based on primary learning style."""
    style = learning_style.lower() if learning_style else 'visual'
    distributions = {
        'visual': {
            'visual_percentage': 65.00,
            'auditory_percentage': 15.00,
            'reading_writing_percentage': 10.00,
            'kinesthetic_percentage': 10.00
        },
        'auditory': {
            'visual_percentage': 15.00,
            'auditory_percentage': 65.00,
            'reading_writing_percentage': 10.00,
            'kinesthetic_percentage': 10.00
        },
        'kinesthetic': {
            'visual_percentage': 10.00,
            'auditory_percentage': 15.00,
            'reading_writing_percentage': 10.00,
            'kinesthetic_percentage': 65.00
        }
    }
    return distributions.get(style, distributions['visual'])

def get_default_profile(learning_style):
    """Get default profile based on primary learning style."""
    style = learning_style.lower() if learning_style else 'visual'
    profiles = {
        'visual': {
            'strengths': 'Visual memory, Pattern recognition, Spatial awareness',
            'areas_for_growth': 'Auditory learning, Note-taking speed'
        },
        'auditory': {
            'strengths': 'Active listening, Group discussions, Verbal explanations',
            'areas_for_growth': 'Visual organization, Written summaries'
        },
        'kinesthetic': {
            'strengths': 'Physical activities, Hands-on experiments, Movement-based learning',
            'areas_for_growth': 'Abstract concepts, Traditional lectures'
        }
    }
    return profiles.get(style, profiles['visual'])

@learning_style_bp.route('/distribution/<int:user_id>', methods=['GET'])
def get_learning_style_distribution(user_id):
    """Get the learning style distribution for a user."""
    cursor = None
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT visual_percentage, auditory_percentage, 
                   reading_writing_percentage, kinesthetic_percentage
            FROM learning_style_distribution
            WHERE userid = %s
        """, (user_id,))
        result = cursor.fetchone()
        if result:
            return jsonify({
                'visual_percentage': float(result[0]),
                'auditory_percentage': float(result[1]),
                'reading_writing_percentage': float(result[2]),
                'kinesthetic_percentage': float(result[3])
            }), 200
        # Return default empty distribution
        return jsonify({
            'visual_percentage': 0.0,
            'auditory_percentage': 0.0,
            'reading_writing_percentage': 0.0,
            'kinesthetic_percentage': 0.0
        }), 200
    except Exception as e:
        # Return empty distribution on error
        return jsonify({
            'visual_percentage': 0.0,
            'auditory_percentage': 0.0,
            'reading_writing_percentage': 0.0,
            'kinesthetic_percentage': 0.0
        }), 200
    finally:
        if cursor:
            cursor.close()

@learning_style_bp.route('/profile/<int:user_id>', methods=['GET'])
def get_learning_profile(user_id):
    """Get the learning profile for a user."""
    cursor = None
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT strengths, areas_for_growth
            FROM learning_style_profile
            WHERE userid = %s
        """, (user_id,))
        result = cursor.fetchone()
        if result:
            return jsonify({
                'strengths': result[0],
                'areas_for_growth': result[1]
            }), 200
        # Return empty profile
        return jsonify({
            'strengths': '',
            'areas_for_growth': ''
        }), 200
    except Exception as e:
        # Return empty profile on error
        return jsonify({
            'strengths': '',
            'areas_for_growth': ''
        }), 200
    finally:
        if cursor:
            cursor.close()

@learning_style_bp.route('/techniques/<string:learning_style>', methods=['GET'])
def get_study_techniques(learning_style):
    """Get study techniques for a specific learning style."""
    cursor = None
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT technique_description
            FROM study_techniques
            WHERE learning_style = %s
        """, (learning_style.lower(),))
        results = cursor.fetchall()
        if results:
            techniques = [{'technique_description': row[0]} for row in results]
            return jsonify(techniques), 200
        # Return empty techniques list
        return jsonify([]), 200
    except Exception as e:
        # Return empty techniques list on error
        return jsonify([]), 200
    finally:
        if cursor:
            cursor.close()

@learning_style_bp.route('/tools/<string:learning_style>', methods=['GET'])
def get_study_tools(learning_style):
    """Get study tools for a specific learning style."""
    cursor = None
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT tool_name, tool_description
            FROM study_tools
            WHERE learning_style = %s
        """, (learning_style.lower(),))
        results = cursor.fetchall()
        if results:
            tools = [{'tool_name': row[0], 'tool_description': row[1]} for row in results]
            return jsonify(tools), 200
        # Return empty tools list
        return jsonify([]), 200
    except Exception as e:
        # Return empty tools list on error
        return jsonify([]), 200
    finally:
        if cursor:
            cursor.close()

@learning_style_bp.route('/recommendations/<string:learning_style>', methods=['GET'])
def get_group_recommendations(learning_style):
    """Get study group recommendations for a specific learning style."""
    cursor = None
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT recommendation_description
            FROM study_group_recommendations
            WHERE learning_style = %s
        """, (learning_style.lower(),))
        results = cursor.fetchall()
        if results:
            recommendations = [{'recommendation_description': row[0]} for row in results]
            return jsonify(recommendations), 200
        # Return empty recommendations list
        return jsonify([]), 200
    except Exception as e:
        # Return empty recommendations list on error
        return jsonify([]), 200
    finally:
        if cursor:
            cursor.close() 