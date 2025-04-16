from flask import Blueprint, request, jsonify
from backend.db_connection import db # Import the db object

# Create a Blueprint for user routes
users = Blueprint('users', __name__)



''' Development route, just want to troubleshoot'''
@users.route('/all', methods=["GET"])
def all_users_and_students_by_naman(): 
    try: 
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall() # fetchall vs fetchone is pretty self explanatory
        return jsonify({"students_or_users" : users}), 200; 
        
    except Exception as e: 
        return jsonify({"error": e}), 404
    




''' needs to be changed to post route. '''
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
            
        # Get database cursor from db object
        cursor = db.get_db().cursor()
        
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
        
        # Connection closing is handled by the extension
        # cursor.close()
        
        return jsonify(results)
        
    except Exception as e:
        # Ensure cursor is closed in case of error if it exists
        if 'cursor' in locals() and cursor is not None:
            cursor.close()
        return jsonify({'error': str(e)}), 500





''' too find a user's resources given PK user_id, can also add a resource DO THIS ON THE FRONTEND.'''
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
    cursor = None # Initialize cursor to None
    try:
        # Get database cursor from db object
        cursor = db.get_db().cursor()
        
        if request.method == 'GET':
            # Query to get all resources for the user
            query = """
                SELECT r.resourceid, r.resource_link, r.resource_type
                FROM resource r 
                JOIN user_resource ur ON r.resourceid = ur.resourceid
                WHERE ur.userid = %s
            """ 
            cursor.execute(query, (user_id,))
            resources = cursor.fetchall()
            
            # cursor.close()
            return jsonify(resources)
            
        elif request.method == 'POST':
            # Get resource data from request
            data = request.get_json()
            if not data or 'link' not in data or 'type' not in data:
                return jsonify({'error': 'link and type are required'}), 400
                
            link = data['link']
            resource_type = data['type']
            
            # Insert new resource using lowercase 'resource'
            query = """
                INSERT INTO resource (resource_link, resource_type)
                VALUES (%s, %s)
            """
            cursor.execute(query, (link, resource_type))
            resource_id = cursor.lastrowid
            
            # Link resource to user using lowercase 'user_resource'
            query = """
                INSERT INTO user_resource (userid, resourceid)
                VALUES (%s, %s)
            """
            cursor.execute(query, (user_id, resource_id))
            
            # Commit the transaction using the db object
            db.get_db().commit()
            
            # cursor.close()
            return jsonify({
                'message': 'Resource added successfully',
                'resource_id': resource_id
            }), 201
            
    except Exception as e:
        # Rollback using the db object
        db.get_db().rollback()
        return jsonify({'error': str(e)}), 500
    
            
            
@users.route('/potential-matches', methods=['POST'])
def get_potential_study_matches(): 
    """Fetches up to 5 potential study matches, excluding the current user."""
    cursor = None # Initialize cursor
    try: 
        data = request.get_json()
        if not data or 'user_id' not in data:
            return jsonify({"error": "Missing 'user_id' in request body"}), 400
            
        current_user_id = data["user_id"]
        
        cursor = db.get_db().cursor()
        # Select relevant user details, exclude the current user, limit to 5
        query = """
            SELECT userid, name, email, major, learning_style, availability 
            FROM user 
            WHERE userid != %s 
            ORDER BY RAND() -- Optional: randomize the selection 
            LIMIT 5
        """
        cursor.execute(query, (current_user_id,))
        potential_matches = cursor.fetchall() 
        
        return jsonify(potential_matches), 200
        
    except Exception as e: 
        # Log the exception for debugging
        # logging.error(f"Error fetching potential matches: {e}") # Assuming logging is set up
        return jsonify({"error": "An internal server error occurred"}), 500
   
    
    
    
@users.route('/groups/all' , methods=['POST'])
def get_all_users_groups():
    """Fetches all study groups (ID and Name) the given user is a member of via the group_student table."""
    cursor = None # Initialize cursor
    try: 
        data = request.get_json()
        # Use 'user_id' to match the key typically sent from frontend/tests
        if not data or data.get("user_id") is None: 
             return jsonify({"error": "Missing or invalid 'user_id' in request body"}), 400
             
        user_id = data["user_id"]
        
        cursor = db.get_db().cursor()
        
        # Query using the group_student junction table
        # Select groupid and group_name from study_group
        query = """
            SELECT 
                sg.groupid, 
                sg.group_name 
            FROM group_student gs
            JOIN study_group sg ON gs.groupid = sg.groupid
            WHERE gs.studentid = %s -- Filter by studentid (user_id)
        """
        
        cursor.execute(query, (user_id,))
        groups = cursor.fetchall() # Fetch all matching groups
            
        return jsonify(groups), 200 # Return the list of group objects {groupid, group_name}
        
    except Exception as e: 
        # Log the exception for debugging
        # logging.error(f"Error fetching user groups: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500
   
            
            
@users.route('/groups/find', methods=['GET'])
def browse_groups(): 
    """Fetches all available study groups (ID and Name)."""
    cursor = None # Initialize cursor
    try: 
        cursor = db.get_db().cursor()
        
        # Query to select all groups
        query = """
            SELECT 
                groupid, 
                group_name 
            FROM study_group
            ORDER BY group_name -- oder alphabetically
        """
        
        cursor.execute(query)
        all_groups = cursor.fetchall()
            
        return jsonify(all_groups), 200
        
    except Exception as e: 
        
        return jsonify({"error": e}), 404

@users.route('/groups/create', methods=['POST'])
def create_group():
    """Creates a new study group AND ADDS the creator as a member, so the creator can see it in the my groups section. """
    cursor = None # Initialize cursor
    try: 
        data = request.get_json()
        # Validate input
        if not data or not data.get("group_name") or data.get("user_id") is None:
             return jsonify({"error": "Missing required fields: 'group_name' and 'user_id'"}), 400
             
        group_name = data["group_name"]
        user_id = data["user_id"]
        
        conn = db.get_db() # Get connection ?????? this is required why????
        cursor = conn.cursor()
        
        # 1. Insert the new study group
        insert_group_query = """
            INSERT INTO study_group (group_name) 
            VALUES (%s)
        """
        cursor.execute(insert_group_query, (group_name,))
        new_group_id = cursor.lastrowid # Get the ID of the newly inserted group
        
        if not new_group_id:
            # This case should ideally not happen if insertion worked, but good to check
             raise Exception("Failed to retrieve new group ID after insertion.")

        # 2. Add the creator to the group via the junction table
        insert_member_query = """
            INSERT INTO group_student (groupid, studentid) 
            VALUES (%s, %s)
        """
        cursor.execute(insert_member_query, (new_group_id, user_id))
        
        # Commit both insertions as a transaction
        conn.commit()
            
        # Return success response with new group details
        return jsonify({ 
            "message": "Study group created successfully!",
            "group": { 
                "groupid": new_group_id,
                "group_name": group_name
            }
        }), 201 # 201 is Created status code
        
    except Exception as e: 
        return jsonify({"error": e}), 404
    


@users.route('/match/all-matches', methods=["GET"])
def get_all_possible_matches(): 
    try: 
        cursor = db.get_db().cursor()
        cursor.execute("SELECT * FROM user")
        users = cursor.fetchall() # fetchall vs fetchone is pretty self explanatory
        return jsonify({"students_or_users" : users}), 200; 
        
    except Exception as e: 
        return jsonify({"error": e}), 404
    
    
@users.route('/match/success', methods=['POST'])
def record_match_success():
    """Records a successful match between two users in the matched_with table."""
    cursor = None # cursror to get data fromd atabase
    conn = None   # conn, or connection, to commit() data into the database. 
    try:
        data = request.get_json()
                 
        #  input VALIDAtion!
        if not data or data.get("user1_id") is None or data.get("user2_id") is None:
              return jsonify({"error": "missing required fields develop better'"}), 400
  
        user_a_id = data["user1_id"]
        user_b_id = data["user2_id"]
        
        # Ensure IDs are distinct
        if user_a_id == user_b_id:
            return jsonify({"error": "Cannot match a user with themselves"}), 400
            
        # Enforce order for consistency (user1_id < user2_id)
        if user_a_id < user_b_id:
            user1_id = user_a_id
            user2_id = user_b_id
        else:
            user1_id = user_b_id # Swap them
            user2_id = user_a_id
          
        conn = db.get_db() # Get connection which i need to commit to the database later. 
        cursor = conn.cursor()
        
        # Insert the match pair into the junction table (ordered)
        # Use INSERT IGNORE to gracefully handle potential duplicate entries 
        insert_match_query = """
            INSERT IGNORE INTO matched_with (user1_id, user2_id) 
            VALUES (%s, %s)
        """
        # Execute insertion with ordered IDs
        rows_affected = cursor.execute(insert_match_query, (user1_id, user2_id))
        
        # Commit the transaction
        conn.commit()
            
        if rows_affected > 0:
            message = "Match recorded successfully!"
        else:
            message = "Match already exists."
            
        # Return success response 
        return jsonify({ "message": message }), 200 # Or 201 if you prefer for new inserts
        
    except Exception as e: 
        # Rollback transaction in case of any error
        if conn: 
            conn.rollback()
        # Log the exception for debugging
        # logging.error(f"Error recording match: {e}")
        return jsonify({"error": f"An internal server error occurred: {str(e)}"}), 500
    finally:
        if cursor is not None:
            cursor.close()



@users.route('/match/<int:user_id>/matches', methods=['GET'])
def get_user_matches(user_id):
    """Fetches the unique names and IDs of users matched with the given user_id."""
    cursor = None # Initialize cursor
    try:
        cursor = db.get_db().cursor()
        
        # Query to find unique names of matched users
        # Use DISTINCT on the selected columns representing the other user
        query = """
            SELECT DISTINCT
                CASE
                    WHEN mw.user1_id = %s THEN u2.name
                    ELSE u1.name
                END AS matched_user_name,
                CASE
                    WHEN mw.user1_id = %s THEN u2.userid
                    ELSE u1.userid
                END AS matched_user_id
            FROM matched_with mw
            JOIN user u1 ON mw.user1_id = u1.userid
            JOIN user u2 ON mw.user2_id = u2.userid
            WHERE mw.user1_id = %s OR mw.user2_id = %s
        """
        
        cursor.execute(query, (user_id, user_id, user_id, user_id))
        matches = cursor.fetchall()
            
        return jsonify(matches), 200
        
    except Exception as e: 
        # Log the exception for debugging
        # logging.error(f"Error fetching user matches: {e}")
        return jsonify({"error": "An internal server error occurred"}), 500
    finally:
        if cursor is not None:
            cursor.close()


