from flask import Blueprint, jsonify
from database import db

analyst_bp = Blueprint('analyst', __name__)

@analyst_bp.route('/a/analytics/interests', methods=['GET'])
def get_interest_distribution():
    try:
        # Execute raw SQL query
        cursor = db.cursor()
        query = """
            SELECT interest, COUNT(*) as count
            FROM user_interests
            GROUP BY interest
            ORDER BY count DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Format the results
        distribution = [
            {'interest': interest, 'count': count}
            for interest, count in results
        ]
        
        return jsonify({
            'status': 'success',
            'distribution': distribution
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@analyst_bp.route('/a/analytics/major-distribution', methods=['GET'])
def get_major_distribution():
    try:
        # Execute raw SQL query
        cursor = db.cursor()
        query = """
            SELECT major, COUNT(*) as count
            FROM user
            GROUP BY major
            ORDER BY count DESC
        """
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Format the results
        distribution = [
            {'major': major, 'count': count}
            for major, count in results
        ]
        
        return jsonify({
            'status': 'success',
            'distribution': distribution
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

# ... existing routes ... 