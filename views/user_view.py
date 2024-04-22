from flask import Blueprint, request, jsonify
from helpers.token_validation import validateJWT
import json
from helpers.utils import validateRequestUser, checkEmail
from controllers.user_controller import createUser, loginUser, fetchUsers


user = Blueprint("users", __name__)

@user.route("/v1/users/signup", methods=["POST"])
def signUp():
    try:
        if not request.data:
            return jsonify({"error": 'There is no data in the request' }), 400

        payload = json.loads(request.data)
        if not validateRequestUser(payload):
            return jsonify({"error": 'Invalid or missing user information!' }), 400
            
        if not checkEmail(payload['email']):
            return jsonify({"error": 'Invalid email address!'}), 400  
        
        createdUser = createUser(payload)
        
        if createdUser == 'Duplicate User':
            return jsonify({"error": 'There is already an user with the informed email address!'}), 400
        
        if not createdUser.inserted_id:
            return jsonify({"error": 'Error creating user, please try again' }), 500

        return jsonify({'uid': f'{str(createdUser.inserted_id)}'}), 200

    except ValueError as err:
        return jsonify({"error": 'Error creating user, please try again'}), 400

@user.route("/v1/users/login", methods=["POST"])
def login():
    try:
        if not request.data:
            raise 'Request error'

        payload = json.loads(request.data)

        if 'email' not in payload:
            return jsonify({"error": 'Email not found in the request'}), 400  

        if 'password' not in payload:
            return jsonify({"error": 'Password not found in the request'}), 400     

        loginAttempt = loginUser(payload)

        if loginAttempt == 'Invalid password':
            return jsonify({"error": 'Invalid credentials'}), 401  

        if loginAttempt == 'Invalid email':
            return jsonify({"error": 'There is no user with the email provided'}), 401            

        return jsonify({'token': loginAttempt.json['token'] , 'expiration': loginAttempt.json['expiration'], 'loggedUser': loginAttempt.json['loggedUser']}), 200

    except ValueError:
        return jsonify({"error": 'Error creating login session, please try again'}), 400

@user.route("/v1/users/all", methods=["GET"])
def all():
    try:
        token = validateJWT()

        if token == 400:
            return jsonify({"error": 'Token is missing in the request, please try again'}), 401

        if token == 401:
            return jsonify({"error": 'Invalid authentication token, please login again'}), 403

        return jsonify(fetchUsers()), 200

    except ValueError:
        return jsonify({"error": 'Error on fetching users, please try again'}), 400