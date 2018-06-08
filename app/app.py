from flask_api import FlaskAPI
from flask import request, jsonify, abort, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity, get_raw_jwt)
from functools import wraps
from flask_jwt_extended import JWTManager
from app.helpers import insert_user, create_request, get_requests, get_user, get_request



# local import
from instance.config import app_config


def create_app(config_name):


    app = FlaskAPI(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])
    

    jwt = JWTManager(app)



    @app.route('/api/v2/auth/signup/', methods=['POST'])
    def signup_user():
        user = {
            'name': request.json.get('name'),
            'email': request.json.get('email'),
            'username': request.json.get('username'),
            'password': request.json.get('password')
        }
        insert_user(user)
        return jsonify({'message': 'New user registered!'})


    @app.route('/api/v2/auth/signin/', methods=['POST'])
    def signin():
        username = request.json.get("username")
        password = request.json.get("password")

        user = get_user(username)
        if user is None:
            return jsonify({"message": "Username not found"}), 404
        elif user['password'] != password:
            return jsonify({'message': "Incorrect password"}), 400
        else :
            token = create_access_token(identity=request.json.get('username'))
            return jsonify({'message': 'Logged in successfully!', 'token': token})
        return make_response('Could not verify!'), 401


    @app.route('/api/v2/auth/requests/', methods=['POST'])
    @jwt_required
    def api_request():

        username = get_jwt_identity()
        user = get_user(username)

        requests = {
           'name': request.json.get('name'), 
           'description': request.json.get('description'),
            'category': request.json.get('category'), 
            'department': request.json.get('department'),
            "user_id": user['id']
        }
        create_request(requests)
        return jsonify({'Requests' : requests}), 201
        
    @app.route('/api/v2/auth/requests/', methods=['GET']) 
    @jwt_required
    def view_all_requests():
        username = get_jwt_identity()
        user = get_user(username)
        requests = get_requests(user['id'])
        return jsonify({'request': requests})

    @app.route('/api/v2/auth/requests/<int:id>', methods=['GET'])
    @jwt_required
    def single_api_request(id):
        username = get_jwt_identity()
        user = get_user(username)
        # retrieve a request using it's ID
        requests = get_request(id)
        return jsonify({'request': requests})

    @app.route('/api/v2/auth/requests/<int:id>', methods=['PUT'])
    @jwt_required
    def api_request_modified(id):
        username = get_jwt_identity()
        user = get_user(username)
        # retrieve a request using it's ID
        edit_requests = get_request(user['id'])
        if edit_requests is None:
            return jsonify({'message': 'Request not found!'})
        edit_request = edit_requests[0]
        edit_request['name']= request.json.get('name')
        edit_request['description'] = request.json.get('description')
        edit_request['category']= request.json.get('category')
        edit_request['department']=request.json.get('department')

        return jsonify({'requests' : edit_request})


    @app.route('/api/v2/auth/requests/<int:id>', methods=['DELETE'])
    @jwt_required
    def api_request_deleted(id):
        delete_request = [request for request in requests if request['id'] == id]
        print(len(delete_request))
        if len(delete_request) == 0:
            abort(404)
        requests.remove(delete_request[0])

        return jsonify({'requests' : requests})

    @app.route('/api/v2/auth/signout/', methods=['POST'])
    @jwt_required
    def signout():
        return jsonify({'message': 'Logged out successfully!'})

    return app