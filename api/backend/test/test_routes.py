from flask import Blueprint, request, jsonify
import logging

from backend.db_connection import db # Assuming db object is set up for queries

test = Blueprint('test', __name__)


@test.route('/test', methods=['GET'])
def test_route():
    return jsonify({"message": "Test route is working"}), 200
