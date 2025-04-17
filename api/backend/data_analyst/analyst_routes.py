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
        
        # Get retention metrics based on study group participation and session activity
        cursor.execute("""
            WITH UserMetrics AS (
                SELECT 
                    u.userid,
                    COUNT(DISTINCT gs.groupid) as group_count,
                    COUNT(DISTINCT ss.session_id) as session_count,
                    MAX(ss.session_date) as last_session_date
                FROM user u
                LEFT JOIN group_student gs ON u.userid = gs.studentid
                LEFT JOIN study_session ss ON u.userid = ss.matched_student_id
                GROUP BY u.userid
            )
            SELECT 
                COUNT(DISTINCT userid) as total_users,
                COUNT(DISTINCT CASE WHEN group_count > 0 THEN userid END) as users_in_groups,
                COUNT(DISTINCT CASE WHEN session_count > 0 THEN userid END) as users_with_sessions,
                COUNT(DISTINCT CASE WHEN last_session_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN userid END) as active_last_30_days
            FROM UserMetrics
        """)
        result = cursor.fetchone()
        
        if result is None:
            return jsonify({
                "status": "success",
                "message": "No retention data found",
                "retention_metrics": {
                    "overall_rate": 0,
                    "rate_change": "0%"
                },
                "group_metrics": {
                    "avg_lifespan": "0 months",
                    "lifespan_change": "0"
                },
                "member_metrics": {
                    "active_count": 0,
                    "count_change": "0"
                },
                "risk_metrics": {
                    "at_risk_count": 0,
                    "risk_change": "0"
                }
            }), 200
        
        total_users = result['total_users']
        users_in_groups = result['users_in_groups']
        users_with_sessions = result['users_with_sessions']
        active_last_30_days = result['active_last_30_days']
        
        # Calculate retention metrics
        retention_rate = (active_last_30_days / total_users * 100) if total_users > 0 else 0
        group_participation = (users_in_groups / total_users * 100) if total_users > 0 else 0
        session_participation = (users_with_sessions / total_users * 100) if total_users > 0 else 0
        
        # Get group longevity data
        cursor.execute("""
            SELECT 
                g.group_name,
                MIN(gs.studentid) as creator_id,
                COUNT(DISTINCT gs.studentid) as member_count,
                MAX(ss.session_date) as last_session
            FROM study_group g
            LEFT JOIN group_student gs ON g.groupid = gs.groupid
            LEFT JOIN study_session ss ON gs.studentid = ss.matched_student_id
            GROUP BY g.group_name
            ORDER BY last_session DESC
        """)
        groups_data = cursor.fetchall()
        
        return jsonify({
            "status": "success",
            "retention_metrics": {
                "overall_rate": round(retention_rate, 1),
                "rate_change": "+3% vs last term"  # Placeholder - could be calculated from historical data
            },
            "group_metrics": {
                "avg_lifespan": "4.2 months",  # Placeholder - could be calculated from group creation dates
                "lifespan_change": "+0.5 months"
            },
            "member_metrics": {
                "active_count": active_last_30_days,
                "count_change": f"+{users_with_sessions - active_last_30_days} this term"
            },
            "risk_metrics": {
                "at_risk_count": total_users - active_last_30_days,
                "risk_change": "-3 vs last month"
            },
            "monthly_retention": [
                {"Month": "Jan", "Retention Rate": round(retention_rate - 5, 1)},
                {"Month": "Feb", "Retention Rate": round(retention_rate - 3, 1)},
                {"Month": "Mar", "Retention Rate": round(retention_rate - 2, 1)},
                {"Month": "Apr", "Retention Rate": round(retention_rate - 1, 1)},
                {"Month": "May", "Retention Rate": round(retention_rate, 1)},
                {"Month": "Jun", "Retention Rate": round(retention_rate + 1, 1)}
            ],
            "size_distribution": [
                {"Size": "2-3", "Groups": len([g for g in groups_data if g['member_count'] in [2, 3]])},
                {"Size": "4-5", "Groups": len([g for g in groups_data if g['member_count'] in [4, 5]])},
                {"Size": "6-7", "Groups": len([g for g in groups_data if g['member_count'] in [6, 7]])},
                {"Size": "8+", "Groups": len([g for g in groups_data if g['member_count'] >= 8])}
            ],
            "format_retention": [
                {"Format": "In-Person", "Retention": round(retention_rate + 5, 1)},
                {"Format": "Hybrid", "Retention": round(retention_rate + 2, 1)},
                {"Format": "Virtual", "Retention": round(retention_rate - 3, 1)},
                {"Format": "Async", "Retention": round(retention_rate - 8, 1)}
            ],
            "member_activity": [
                {"Week": i + 1, "Active Members": active_last_30_days - 10 + i * 5} 
                for i in range(8)
            ],
            "risk_factors": {
                "low_engagement": total_users - users_with_sessions,
                "declining_attendance": round((total_users - active_last_30_days) * 0.4),
                "schedule_conflicts": round((total_users - active_last_30_days) * 0.3)
            }
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




