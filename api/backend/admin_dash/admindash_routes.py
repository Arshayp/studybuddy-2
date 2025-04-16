from flask import Blueprint, request, jsonify
import logging


from backend.db_connection import db # Assuming db object is set up for queries

admin = Blueprint('admin_dashboard', __name__)


# Route to get all admins (returns list of dictionaries)
@admin.route('/all', methods=['GET'])
def get_all_admins_main(): 
    try:
        conn = db.get_db()
        if not conn:
            logging.error("Failed to get DB connection in /all route.")
            return jsonify({"error": "Database connection failed"}), 500
            
        # Use a dictionary cursor if available (preferred)
        try:
            cursor = conn.cursor(dictionary=True) 
        except TypeError:
            # Fallback if dictionary cursor isn't supported directly
            cursor = conn.cursor()

        cursor.execute("SELECT adminid, name, email, role FROM admin") 
        admins = cursor.fetchall()
        
        # If not using dictionary cursor, format manually
        if not isinstance(admins[0], dict) and len(admins) > 0:
             admin_list = [
                 {'adminid': row[0], 'name': row[1], 'email': row[2], 'role': row[3]}
                 for row in admins
             ]
             admins = admin_list # Overwrite with the list of dicts
                
        return jsonify({"admins": admins}), 200
    
    except Exception as e:
        logging.error(f"Error fetching admins in /all route: {e}")
        return jsonify({"error": "Failed to fetch admins"}), 500

# Route to get all regular users (returns list of dictionaries)
@admin.route('/users', methods=['GET'])
def get_all_users():
    try:
        conn = db.get_db()
        if not conn:
            logging.error("Failed to get DB connection in GET /users route.")
            return jsonify({"error": "Database connection failed"}), 500
        
        # Use a dictionary cursor if available
        try:
            cursor = conn.cursor(dictionary=True)
        except TypeError:
            cursor = conn.cursor()
        
        # Select relevant user fields (avoiding password)
        cursor.execute("SELECT userid, name, email, major, learning_style, availability FROM user")
        users = cursor.fetchall()

        # If not using dictionary cursor, format manually
        if not isinstance(users[0], dict) and len(users) > 0:
            user_list = [
                {'userid': row[0], 'name': row[1], 'email': row[2], 'major': row[3], 'learning_style': row[4], 'availability': row[5]}
                for row in users
            ]
            users = user_list
        
        return jsonify({"users": users}), 200
    
    except Exception as e:
        logging.error(f"Error fetching users in GET /users route: {e}")
        return jsonify({"error": "Failed to fetch users"}), 500

# Route to add a new regular user (using correct table name 'user')
@admin.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    if not data or not all(k in data for k in ('name', 'email', 'password')):
        return jsonify({"error": "Missing data: name, email, and password required"}), 400

    name = data['name']
    email = data['email']
    password = data['password'] 

    try:
        conn = db.get_db()
        if not conn:
             logging.error("Failed to get DB connection in /users route.")
             return jsonify({"error": "Database connection error"}), 500
        cursor = conn.cursor()
        # Use correct table name 'user'
        cursor.execute("INSERT INTO user (name, email, password) VALUES (%s, %s, %s)", 
                       (name, email, password)) 
        conn.commit()
        # Get the ID of the newly inserted user
        new_user_id = cursor.lastrowid 
        return jsonify({"message": f"User '{name}' created successfully.", "userid": new_user_id}), 201
    except Exception as e:
        # Make sure conn is defined for rollback
        if conn:
             conn.rollback() # Rollback in case of error
        logging.error(f"Error adding user: {e}")
        # Check for duplicate email error (MySQL specific error code 1062)
        if "1062" in str(e):
             return jsonify({"error": f"Email '{email}' already exists."}), 409 # Conflict
        return jsonify({"error": "Failed to create user"}), 500

# Route to add a new admin (using correct columns: name, role, email)
@admin.route('/admins', methods=['POST'])
def add_admin():
    data = request.get_json()
    # Expect name, role, email for admin table
    if not data or not all(k in data for k in ('name', 'role', 'email')):
        return jsonify({"error": "Missing data: name, role, and email required"}), 400

    name = data['name']
    role = data['role']
    email = data['email']

    try:
        conn = db.get_db()
        if not conn:
             logging.error("Failed to get DB connection in /admins route.")
             return jsonify({"error": "Database connection error"}), 500
        cursor = conn.cursor()
        # Use correct columns for admin table
        cursor.execute("INSERT INTO admin (name, role, email) VALUES (%s, %s, %s)", 
                       (name, role, email)) 
        conn.commit()
        # Get the ID of the newly inserted admin
        new_admin_id = cursor.lastrowid
        return jsonify({"message": f"Admin '{name}' created successfully.", "adminid": new_admin_id}), 201
    except Exception as e:
        # Make sure conn is defined for rollback
        if conn:
            conn.rollback()
        logging.error(f"Error adding admin: {e}")
        if "1062" in str(e):
             return jsonify({"error": f"Admin email '{email}' already exists."}), 409
        return jsonify({"error": "Failed to create admin"}), 500

# --- DELETE User ---
@admin.route('/users/<int:userid>', methods=['DELETE'])
def delete_user(userid):
    try:
        conn = db.get_db()
        cursor = conn.cursor()
        
        # Check if user exists before deleting
        cursor.execute("DELETE FROM user WHERE userid = %s", (userid,))
        
        if cursor.rowcount == 0:
            return jsonify({"error": f"User with ID {userid} not found."}), 404
            
        conn.commit()
        logging.info(f"Deleted user with ID: {userid}")
        return jsonify({"message": f"User with ID {userid} deleted successfully."}), 200
    except Exception as e:
        if conn:
             conn.rollback()
        logging.error(f"Error deleting user {userid}: {e}")
        # Foreign key constraint errors might occur if user is linked elsewhere
        return jsonify({"error": "Failed to delete user"}), 500

# --- UPDATE User ---
@admin.route('/users/<int:userid>', methods=['PUT'])
def update_user(userid):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing update data"}), 400

    # Build the SET part of the SQL query dynamically
    # Only include fields provided in the request body
    # Be careful about which fields are allowed to be updated!
    # Exclude password updates via this route for simplicity/security unless specifically required
    allowed_fields = ['name', 'email', 'major', 'learning_style', 'availability'] 
    set_clauses = []
    values = []

    for field in allowed_fields:
        if field in data:
            set_clauses.append(f"{field} = %s")
            values.append(data[field])
            
    if not set_clauses:
         return jsonify({"error": "No valid fields provided for update."}), 400

    # Add the userid to the end of the values list for the WHERE clause
    values.append(userid)

    sql = f"UPDATE user SET {', '.join(set_clauses)} WHERE userid = %s"

    try:
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute(sql, tuple(values))
        
        if cursor.rowcount == 0:
            return jsonify({"error": f"User with ID {userid} not found or no changes made."}), 404 # Or 200/304 if no change is ok
            
        conn.commit()
        logging.info(f"Updated user with ID: {userid}")
        return jsonify({"message": f"User {userid} updated successfully."}), 200
    except Exception as e:
        if conn:
             conn.rollback()
        logging.error(f"Error updating user {userid}: {e}")
        if "1062" in str(e): # Check for duplicate email
             return jsonify({"error": f"Email '{data.get('email')}' already exists."}), 409
        return jsonify({"error": "Failed to update user"}), 500

# --- DELETE Admin ---
@admin.route('/admins/<int:adminid>', methods=['DELETE'])
def delete_admin(adminid):
    try:
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM admin WHERE adminid = %s", (adminid,))
        
        if cursor.rowcount == 0:
            return jsonify({"error": f"Admin with ID {adminid} not found."}), 404

        conn.commit()
        logging.info(f"Deleted admin with ID: {adminid}")
        return jsonify({"message": f"Admin with ID {adminid} deleted successfully."}), 200
    except Exception as e:
        if conn:
             conn.rollback()
        logging.error(f"Error deleting admin {adminid}: {e}")
        # Consider foreign key constraints (e.g., systemlog)
        return jsonify({"error": "Failed to delete admin"}), 500

# --- UPDATE Admin ---
@admin.route('/admins/<int:adminid>', methods=['PUT'])
def update_admin(adminid):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing update data"}), 400

    # Define allowed fields for admin update
    allowed_fields = ['name', 'role', 'email'] 
    set_clauses = []
    values = []

    for field in allowed_fields:
        if field in data:
            set_clauses.append(f"{field} = %s")
            values.append(data[field])
            
    if not set_clauses:
         return jsonify({"error": "No valid fields provided for update."}), 400

    values.append(adminid)
    sql = f"UPDATE admin SET {', '.join(set_clauses)} WHERE adminid = %s"

    try:
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute(sql, tuple(values))
        
        if cursor.rowcount == 0:
            return jsonify({"error": f"Admin with ID {adminid} not found or no changes made."}), 404

        conn.commit()
        logging.info(f"Updated admin with ID: {adminid}")
        return jsonify({"message": f"Admin {adminid} updated successfully."}), 200
    except Exception as e:
        if conn:
             conn.rollback()
        logging.error(f"Error updating admin {adminid}: {e}")
        if "1062" in str(e): # Check for duplicate email
             return jsonify({"error": f"Admin email '{data.get('email')}' already exists."}), 409
        return jsonify({"error": "Failed to update admin"}), 500

# --- GET User Count (Accessing by key) ---
@admin.route('/users/count', methods=['GET'])
def get_user_count():
    conn = None
    cursor = None
    try:
        logging.info("Attempting to get DB connection for user count...")
        conn = db.get_db()
        logging.info(f"DB connection object for user count: {conn}")
        if not conn:
             logging.error("DB connection is None in /users/count")
             return jsonify({"error": "Database connection failed (None)"}), 500
             
        logging.info("Attempting to get cursor for user count...")
        # Assume it might be a dictionary cursor
        cursor = conn.cursor() 
        logging.info(f"Cursor object for user count: {cursor}")
        
        logging.info("Executing user count query...")
        cursor.execute("SELECT COUNT(*) FROM user")
        logging.info("User count query executed.")
        
        logging.info("Fetching user count result...")
        result = cursor.fetchone() # Expects dict {'COUNT(*)': N} or tuple (N,)
        logging.info(f"User count fetchone() result: {result}")
        
        if result is None:
            logging.error("User count fetchone() returned None.")
            return jsonify({"error": "Failed to fetch count result"}), 500

        # Try accessing as dict first, fallback to index
        if isinstance(result, dict):
            count = result.get('COUNT(*)') 
        else:
            count = result[0] # Fallback for standard tuple cursor

        if count is None:
             logging.error(f"Could not find 'COUNT(*)' key or index 0 in result: {result}")
             return jsonify({"error": "Failed to parse count result"}), 500
             
        logging.info(f"User count extracted: {count}")
        return jsonify({"count": count}), 200
    except Exception as e:
        logging.error(f"Error getting user count: {e} (Type: {type(e)})")
        return jsonify({"error": "Failed to get user count"}), 500
    finally:
        if cursor:
            logging.info("Closing user count cursor.")
            cursor.close()

# --- GET Admin Count (Accessing by key) ---
@admin.route('/admins/count', methods=['GET'])
def get_admin_count():
    conn = None
    cursor = None
    try:
        logging.info("Attempting to get DB connection for admin count...")
        conn = db.get_db()
        logging.info(f"DB connection object for admin count: {conn}")
        if not conn:
             logging.error("DB connection is None in /admins/count")
             return jsonify({"error": "Database connection failed (None)"}), 500

        logging.info("Attempting to get cursor for admin count...")
        # Assume it might be a dictionary cursor
        cursor = conn.cursor()
        logging.info(f"Cursor object for admin count: {cursor}")
        
        logging.info("Executing admin count query...")
        cursor.execute("SELECT COUNT(*) FROM admin")
        logging.info("Admin count query executed.")
        
        logging.info("Fetching admin count result...")
        result = cursor.fetchone()
        logging.info(f"Admin count fetchone() result: {result}")

        if result is None:
            logging.error("Admin count fetchone() returned None.")
            return jsonify({"error": "Failed to fetch count result"}), 500

        # Try accessing as dict first, fallback to index
        if isinstance(result, dict):
            count = result.get('COUNT(*)')
        else:
            count = result[0] # Fallback for standard tuple cursor
            
        if count is None:
             logging.error(f"Could not find 'COUNT(*)' key or index 0 in result: {result}")
             return jsonify({"error": "Failed to parse count result"}), 500
             
        logging.info(f"Admin count extracted: {count}")
        return jsonify({"count": count}), 200
    except Exception as e:
        logging.error(f"Error getting admin count: {e} (Type: {type(e)})")
        return jsonify({"error": "Failed to get admin count"}), 500
    finally:
        if cursor:
            logging.info("Closing admin count cursor.")
            cursor.close()



