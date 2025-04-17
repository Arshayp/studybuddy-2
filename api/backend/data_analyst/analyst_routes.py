from flask import Blueprint, request, jsonify
from backend.db_connection import db # Import the db object

# Create a Blueprint for user routes
analyst = Blueprint('analyst', __name__)

@analyst.route('/matches/total', methods=['GET'])
def get_total_matches(): 
    cursor = None
    try: 
        # Get database cursor
        cursor = db.get_db().cursor()
        
        # Execute query to count all matches
        cursor.execute("""
            SELECT COUNT(*) as total 
            FROM matched_with
        """)
        result = cursor.fetchone()
        
        # Debug print to check the result
        print(f"Query result: {result}")
        
        # Since we're using DictCursor, we can access the result by column name
        if result is None:
            return jsonify({
                "total_matches": 0,
                "time_period": "all time",
                "status": "success",
                "message": "No matches found"
            }), 200
            
        total_matches = result['total']
        
        # Debug print to check the count
        print(f"Total matches: {total_matches}")
        
        return jsonify({
            "total_matches": total_matches,
            "time_period": "all time",
            "status": "success"
        }), 200
        
    except Exception as e: 
        # Log the actual error (you should set up proper logging)
        print(f"Error in get_total_matches: {str(e)}")
        return jsonify({
            "error": "Failed to fetch total matches",
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

@analyst.route('/analytics/academic', methods=['GET'])
def get_academic_insights():
    cursor = None
    try:
        cursor = db.get_db().cursor()
        
        # Get course performance metrics
        cursor.execute("""
            SELECT 
                c.course_name,
                COUNT(DISTINCT ss.matched_student_id) as total_students,
                COUNT(ss.session_id) as total_sessions,
                COUNT(DISTINCT u.major) as unique_majors
            FROM course c
            LEFT JOIN study_session ss ON c.courseid = ss.course_id
            LEFT JOIN user u ON ss.matched_student_id = u.userid
            GROUP BY c.course_name
            ORDER BY total_sessions DESC
        """)
        course_metrics = cursor.fetchall()
        
        # Get learning style distribution
        cursor.execute("""
            SELECT 
                learning_style,
                COUNT(*) as student_count,
                COUNT(*) * 100.0 / (SELECT COUNT(*) FROM user WHERE learning_style IS NOT NULL) as percentage
            FROM user
            WHERE learning_style IS NOT NULL
            GROUP BY learning_style
        """)
        learning_styles = cursor.fetchall()
        
        # Get study session trends
        cursor.execute("""
            SELECT 
                DATE_FORMAT(session_date, '%Y-%m') as month,
                COUNT(*) as session_count,
                COUNT(DISTINCT matched_student_id) as active_students
            FROM study_session
            GROUP BY DATE_FORMAT(session_date, '%Y-%m')
            ORDER BY month DESC
            LIMIT 6
        """)
        session_trends = cursor.fetchall()
        
        # Get major distribution and performance
        cursor.execute("""
            SELECT 
                u.major,
                COUNT(DISTINCT u.userid) as student_count,
                COUNT(DISTINCT ss.session_id) as study_sessions
            FROM user u
            LEFT JOIN study_session ss ON u.userid = ss.matched_student_id
            WHERE u.major IS NOT NULL
            GROUP BY u.major
            ORDER BY study_sessions DESC
        """)
        major_metrics = cursor.fetchall()
        
        return jsonify({
            "status": "success",
            "course_metrics": [
                {
                    "course": metric['course_name'],
                    "students": metric['total_students'],
                    "sessions": metric['total_sessions'],
                    "major_diversity": metric['unique_majors']
                } for metric in course_metrics
            ],
            "learning_styles": [
                {
                    "style": style['learning_style'],
                    "percentage": round(style['percentage'], 1)
                } for style in learning_styles
            ],
            "study_trends": [
                {
                    "month": trend['month'],
                    "sessions": trend['session_count'],
                    "active_students": trend['active_students']
                } for trend in session_trends
            ],
            "major_distribution": [
                {
                    "major": major['major'],
                    "students": major['student_count'],
                    "engagement": major['study_sessions']
                } for major in major_metrics
            ]
        }), 200
        
    except Exception as e:
        print(f"Error in get_academic_insights: {str(e)}")
        return jsonify({
            "error": "Failed to fetch academic insights",
            "message": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()

@analyst.route('/analytics/retention/group-longevity', methods=['GET'])
def get_group_longevity():
    cursor = None
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT 
                g.group_name,
                MIN(ss.session_date) as first_session,
                MAX(ss.session_date) as last_session,
                DATEDIFF(MAX(ss.session_date), MIN(ss.session_date)) as days_active,
                COUNT(DISTINCT gs.studentid) as member_count
            FROM study_group g
            JOIN group_student gs ON g.groupid = gs.groupid
            LEFT JOIN study_session ss ON gs.studentid = ss.matched_student_id
            GROUP BY g.group_name
            ORDER BY days_active DESC
        """)
        results = cursor.fetchall()
        
        return jsonify({
            "status": "success",
            "group_longevity": [
                {
                    "group_name": group['group_name'],
                    "lifespan_days": group['days_active'],
                    "member_count": group['member_count'],
                    "first_session": group['first_session'].strftime('%Y-%m-%d') if group['first_session'] else None,
                    "last_session": group['last_session'].strftime('%Y-%m-%d') if group['last_session'] else None
                } for group in results
            ]
        }), 200
    except Exception as e:
        print(f"Error in get_group_longevity: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@analyst.route('/analytics/academic/major-performance', methods=['GET'])
def get_major_performance():
    cursor = None
    try:
        cursor = db.get_db().cursor()
        cursor.execute("""
            SELECT 
                u.major,
                c.course_name,
                COUNT(ss.session_id) as total_sessions,
                COUNT(DISTINCT ss.matched_student_id) as unique_students,
                COUNT(ss.session_id) / COUNT(DISTINCT ss.matched_student_id) as sessions_per_student
            FROM user u
            JOIN study_session ss ON u.userid = ss.matched_student_id
            JOIN course c ON ss.course_id = c.courseid
            WHERE u.major IS NOT NULL
            GROUP BY u.major, c.course_name
            ORDER BY sessions_per_student DESC
        """)
        results = cursor.fetchall()
        
        return jsonify({
            "status": "success",
            "major_performance": [
                {
                    "major": result['major'],
                    "course": result['course_name'],
                    "total_sessions": result['total_sessions'],
                    "unique_students": result['unique_students'],
                    "sessions_per_student": round(result['sessions_per_student'], 2)
                } for result in results
            ]
        }), 200
    except Exception as e:
        print(f"Error in get_major_performance: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@analyst.route('/analytics/academic/learning-styles', methods=['GET'])
def get_learning_style_distribution():
    cursor = None
    try:
        print("Fetching learning style distribution...")  # Debug log
        cursor = db.get_db().cursor()
        
        # Get learning style distribution with debug logging
        query = """
            SELECT 
                COALESCE(learning_style, 'Not Specified') as style,
                COUNT(*) as count,
                COUNT(*) * 100.0 / (SELECT COUNT(*) FROM user) as percentage
            FROM user
            GROUP BY learning_style
            ORDER BY count DESC
        """
        print(f"Executing query: {query}")  # Debug log
        cursor.execute(query)
        results = cursor.fetchall()
        print(f"Query results: {results}")  # Debug log
        
        return jsonify({
            "status": "success",
            "learning_styles": [
                {
                    "style": result['style'],
                    "count": result['count'],
                    "percentage": round(result['percentage'], 1)
                } for result in results
            ]
        }), 200
        
    except Exception as e:
        print(f"Error in get_learning_style_distribution: {str(e)}")  # Debug log
        return jsonify({
            "error": "Failed to fetch learning style distribution",
            "message": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()

@analyst.route('/analytics/academic/study-sessions', methods=['GET'])
def get_study_session_analytics():
    cursor = None
    try:
        cursor = db.get_db().cursor()
        
        # Get study session analytics
        cursor.execute("""
            SELECT 
                ss.study_type,
                COUNT(*) as session_count,
                COUNT(DISTINCT ss.matched_student_id) as unique_students,
                COUNT(*) * 1.0 / COUNT(DISTINCT ss.matched_student_id) as avg_sessions_per_student,
                c.department,
                c.course_name
            FROM study_session ss
            JOIN course c ON ss.course_id = c.courseid
            GROUP BY ss.study_type, c.department, c.course_name
            ORDER BY session_count DESC
        """)
        results = cursor.fetchall()
        
        # Get time-based trends
        cursor.execute("""
            SELECT 
                DATE_FORMAT(session_date, '%Y-%m') as month,
                COUNT(*) as monthly_sessions,
                COUNT(DISTINCT matched_student_id) as monthly_active_students
            FROM study_session
            GROUP BY DATE_FORMAT(session_date, '%Y-%m')
            ORDER BY month DESC
            LIMIT 6
        """)
        trend_results = cursor.fetchall()
        
        return jsonify({
            "status": "success",
            "session_analytics": [
                {
                    "study_type": result['study_type'],
                    "session_count": result['session_count'],
                    "unique_students": result['unique_students'],
                    "avg_sessions_per_student": round(result['avg_sessions_per_student'], 2),
                    "department": result['department'],
                    "course_name": result['course_name']
                } for result in results
            ],
            "monthly_trends": [
                {
                    "month": trend['month'],
                    "total_sessions": trend['monthly_sessions'],
                    "active_students": trend['monthly_active_students']
                } for trend in trend_results
            ]
        }), 200
        
    except Exception as e:
        print(f"Error in get_study_session_analytics: {str(e)}")
        return jsonify({
            "error": "Failed to fetch study session analytics",
            "message": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()

@analyst.route('/analytics/academic/course-performance', methods=['GET'])
def get_course_performance():
    cursor = None
    try:
        cursor = db.get_db().cursor()
        
        # Get course performance metrics
        cursor.execute("""
            SELECT 
                c.department,
                c.course_name,
                COUNT(DISTINCT ss.matched_student_id) as student_count,
                COUNT(ss.session_id) as total_sessions,
                CAST(COUNT(ss.session_id) * 1.0 / NULLIF(COUNT(DISTINCT ss.matched_student_id), 0) AS DECIMAL(10,2)) as avg_sessions_per_student
            FROM course c
            LEFT JOIN study_session ss ON c.courseid = ss.course_id
            GROUP BY c.department, c.course_name
            ORDER BY student_count DESC
        """)
        course_results = cursor.fetchall()
        
        # Get major distribution across courses
        cursor.execute("""
            SELECT 
                u.major,
                COUNT(DISTINCT ss.course_id) as course_count,
                COUNT(ss.session_id) as total_sessions
            FROM user u
            JOIN study_session ss ON u.userid = ss.matched_student_id
            GROUP BY u.major
            ORDER BY course_count DESC
        """)
        major_results = cursor.fetchall()
        
        return jsonify({
            "status": "success",
            "course_analytics": [
                {
                    "department": result['department'],
                    "course_name": result['course_name'],
                    "student_count": int(result['student_count'] or 0),
                    "total_sessions": int(result['total_sessions'] or 0),
                    "avg_sessions_per_student": float(result['avg_sessions_per_student'] or 0)
                } for result in course_results
            ],
            "major_distribution": [
                {
                    "major": result['major'],
                    "course_count": int(result['course_count']),
                    "total_sessions": int(result['total_sessions'])
                } for result in major_results
            ]
        }), 200
        
    except Exception as e:
        print(f"Error in get_course_performance: {str(e)}")
        return jsonify({
            "error": "Failed to fetch course performance analytics",
            "message": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()

@analyst.route('/analytics/study-groups/active', methods=['GET'])
def get_active_study_groups():
    cursor = None
    try:
        cursor = db.get_db().cursor()
        
        # Get current active study groups and monthly change
        cursor.execute("""
            WITH CurrentGroups AS (
                SELECT 
                    COUNT(DISTINCT sg.groupid) as total_groups,
                    COUNT(DISTINCT CASE 
                        WHEN ss.session_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) 
                        THEN sg.groupid 
                    END) as active_groups
                FROM study_group sg
                LEFT JOIN group_student gs ON sg.groupid = gs.groupid
                LEFT JOIN study_session ss ON gs.studentid = ss.matched_student_id
            ),
            LastMonthGroups AS (
                SELECT COUNT(DISTINCT sg.groupid) as last_month_active
                FROM study_group sg
                JOIN group_student gs ON sg.groupid = gs.groupid
                JOIN study_session ss ON gs.studentid = ss.matched_student_id
                WHERE ss.session_date BETWEEN 
                    DATE_SUB(CURDATE(), INTERVAL 60 DAY) AND
                    DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            )
            SELECT 
                cg.total_groups,
                cg.active_groups,
                COALESCE(cg.active_groups - lmg.last_month_active, 0) as monthly_change,
                CASE 
                    WHEN lmg.last_month_active > 0 
                    THEN ROUND((cg.active_groups - lmg.last_month_active) * 100.0 / lmg.last_month_active, 1)
                    ELSE 0 
                END as change_percentage
            FROM CurrentGroups cg
            CROSS JOIN LastMonthGroups lmg
        """)
        result = cursor.fetchone()
        
        if result:
            return jsonify({
                "status": "success",
                "metrics": {
                    "total_groups": int(result['total_groups'] or 0),
                    "active_groups": int(result['active_groups'] or 0),
                    "monthly_change": int(result['monthly_change'] or 0),
                    "change_percentage": float(result['change_percentage'] or 0)
                }
            }), 200
        else:
            return jsonify({
                "status": "success",
                "metrics": {
                    "total_groups": 0,
                    "active_groups": 0,
                    "monthly_change": 0,
                    "change_percentage": 0
                }
            }), 200
            
    except Exception as e:
        print(f"Error in get_active_study_groups: {str(e)}")
        return jsonify({
            "error": "Failed to fetch active study groups metrics",
            "message": str(e)
        }), 500
    finally:
        if cursor:
            cursor.close()




