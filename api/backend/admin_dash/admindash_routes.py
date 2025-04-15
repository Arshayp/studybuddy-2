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



