from flask import Blueprint, request, jsonify
from backend.db_connection import db # Import the db object

# Create a Blueprint for user routes
analyst = Blueprint('analyst', __name__)

@analyst.route('/matches/total', methods=['GET'])
def get_total_matches():
    """Fetches all established matches from the matched_with table."""
    cursor = None
    try:
        cursor = db.get_db().cursor()

        # Execute query to fetch all matches
        cursor.execute("""
            SELECT user1_id, user2_id, match_date
            FROM matched_with
        """)
        matches = cursor.fetchall() # Fetch all rows

        # Debug print to check the result
        print(f"Query result (matches): {matches}")

        return jsonify({
            "matches": matches, # Return the list of matches
            "status": "success"
        }), 200

    except Exception as e:
        print(f"Error in get_total_matches: {str(e)}")
        return jsonify({
            "error": "Failed to fetch matches",
            "message": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()

@analyst.route('/analytics/retention', methods=['GET'])
def get_retention_rate():
    cursor = None
    try:
        # Get database cursor
        cursor = db.get_db().cursor()
        
        # Execute query to calculate retention rate
        # This is a placeholder query - you'll need to implement the actual retention calculation
        cursor.execute("""
            SELECT 
                COUNT(DISTINCT userid) as active_users,
                COUNT(DISTINCT CASE WHEN last_login > DATE_SUB(NOW(), INTERVAL 30 DAY) THEN userid END) as retained_users
            FROM user
        """)
        result = cursor.fetchone()
        
        if result is None:
            return jsonify({
                "retention_rate": 0,
                "retention_change": "0%",
                "status": "success",
                "message": "No retention data found"
            }), 200
            
        active_users = result['active_users']
        retained_users = result['retained_users']
        
        # Calculate retention rate
        retention_rate = (retained_users / active_users * 100) if active_users > 0 else 0
        
        return jsonify({
            "retention_rate": round(retention_rate, 1),
            "retention_change": "+5%",  # This should be calculated based on historical data
            "status": "success"
        }), 200
        
    except Exception as e:
        print(f"Error in get_retention_rate: {str(e)}")
        return jsonify({
            "error": "Failed to fetch retention data",
            "message": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()




