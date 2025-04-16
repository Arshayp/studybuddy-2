from flask import Blueprint, request, jsonify
import logging

from backend.db_connection import db # Assuming db object is set up for queries

auth = Blueprint('auth', __name__)



# this is a test route just ot test if the blueprint registered properly. 
@auth.route('/login', methods=['GET'])
def example(): 
    cursor = db.get_db().cursor()
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall() # fetchall vs fetchone is pretty self explanatory
    return jsonify({"users" : users}), 200; 




# POST /login - Register a new user
# PUT /login - Log in an existing user
@auth.route('/login', methods=['POST', 'PUT'])
def handle_login():
    if request.method == 'POST': # Registration
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password') or not data.get('name'):
            return jsonify({"error": "Missing required fields (name, email, password)"}), 400

        name = data['name']
        email = data['email']
        password = data['password'] # Storing plain text password UNSAFE FOR PRODuction but fine for now i guess

        # Check if user already exists
        cursor = db.get_db().cursor()
        try:
            cursor.execute("SELECT userid FROM user WHERE email = %s", (email,))
            existing_user = cursor.fetchone()
            if existing_user:
                return jsonify({"error": "User with this email already exists"}), 500 # Conflict

            # Insert new user with plain password
            cursor.execute("INSERT INTO user (name, email, password, major, learning_style, availability) VALUES (%s, %s, %s, %s, %s, %s)", 
                             (name, email, password, data.get('major'), data.get('learning_style'), data.get('availability')))
            db.get_db().commit()
            new_user_id = cursor.lastrowid
            logging.info(f"User {email} registered successfully with ID: {new_user_id}")
            return jsonify({"message": "User registered successfully", "user_id": new_user_id}), 201
        except Exception as e:
            db.get_db().rollback()
            logging.error(f"Error during user registration: {e}")
            return jsonify({"error": "Internal server error during registration"}), 500
        finally:
            cursor.close()

    elif request.method == 'PUT': # Login
        data = request.get_json()
        if not data or not data.get('email') or not data.get('password'):
            return jsonify({"error": "Missing required fields (email, password)"}), 400

        email = data['email']
        password = data['password']

        cursor = db.get_db().cursor()
        try:
            # Retrieve the stored plain text password
            cursor.execute("SELECT userid, password FROM user WHERE email = %s", (email,))
            user = cursor.fetchone() # Returns a dictionary because of DictCursor

            if not user:
                return jsonify({"error": "Invalid email or password"}), 401 # Unauthorized

            # --- Correctly access dictionary keys --- 
            user_id = user['userid']             # Access via key
            stored_password = user['password']     # Access via key
            
            # Direct comparison of plain text passwords
            if stored_password == password:
                return jsonify({"message": "Login successful", "user_id": user_id}), 200
            else:
                return jsonify({"error": "Invalid email or password"}), 401 # Unauthorized
        except Exception as e:
            return jsonify({"error": "Internal server error during login"}), 500
        finally:
            cursor.close() 