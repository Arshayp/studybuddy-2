from flask import Blueprint, request, jsonify
import logging


from backend.db_connection import db # Assuming db object is set up for queries

admin = Blueprint('admin_dashboard', __name__)


# Simplified route to get all admins, mirroring GET /login pattern
@admin.route('/all', methods=['GET'])
def get_all_admins_main(): 
    try:
        conn = db.get_db()
        if not conn:
            logging.error("Failed to get DB connection in /all route.")
            return jsonify({"error": "Database connection failed"}), 500
            
        cursor = conn.cursor() 
        
        # Select all columns from admin table
        cursor.execute("SELECT * FROM admin") 
        
        # Fetchall returns a list of tuples
        admins = cursor.fetchall()
                
        # Return the raw list of tuples directly
        return jsonify({"admins": admins}), 200
    
    except Exception as e:
        # Basic error logging
        logging.error(f"Error fetching admins in /all route: {e}")
        return jsonify({"error": "Failed to fetch admins"}), 500


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



