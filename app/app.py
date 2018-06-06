from flask_api import FlaskAPI
from flask import request, jsonify, abort, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity, get_raw_jwt)
from functools import wraps
from flask_jwt_extended import JWTManager
from app.helpers import  get_users, insert_user, create_request, get_requests



# local import
from instance.config import app_config


def create_app(config_name):


    app = FlaskAPI(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])
    

    jwt = JWTManager(app)



    @app.route('/api/v1/auth/signup/', methods=['POST'])
    def signup_user():
        user = {
            'name': request.json.get('name'),
            'email': request.json.get('email'),
            'username': request.json.get('username'),
            'password': request.json.get('password')
        }
        insert_user(user)
        return jsonify({'message': 'New user registered!'})

    @app.route('/api/v1/auth/signup/', methods=['GET'])
    def get_all_users():
        user = get_users()
        return jsonify({'users': user})

    @app.route('/api/v1/auth/signin/', methods=['POST'])
    def signin():
        if request.authorization and request.authorization.username == request.json.get('username') and request.authorization.password == request.json.get('password'):
            token = create_access_token(identity=request.json.get('username'))
            return jsonify({'message': 'Logged in successfully!', 'token': token})
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required!"'})


    @app.route('/api/v1/auth/requests/', methods=['POST'])
    @jwt_required
    def api_request():

        requests = {
           'name': request.json.get('name'), 
           'description': request.json.get('description'),
            'category': request.json.get('category'), 
            'department': request.json.get('department')
        }
        create_request(requests)
        return jsonify({'Requests' : create_request}), 201
        
    @app.route('/api/v1/user/requests/', methods=['GET']) 
    @jwt_required
    def view_all_requests():
        requests = get_requests()
        return jsonify({'request': requests})

    @app.route('/api/v1/user/requests/<int:id>', methods=['GET'])
    @jwt_required
    def single_api_request(id):
        # retrieve a request using it's ID
        single_request = [request for request in requests if request['id'] == id]

        return jsonify({'request': single_request})

    @app.route('/api/v1/user/requests/<int:id>', methods=['PUT'])
    @jwt_required
    def api_request_modified(id):
        edit_request = [request for request in requests if request['id'] == id]
        if len(edit_request) == 0:
            return jsonify({'message': 'Request not found!'})
        edit_request = edit_request[0]
        edit_request['name']= request.json.get('name')
        edit_request['description'] = request.json.get('description')
        edit_request['category']= request.json.get('category')
        edit_request['department']=request.json.get('department')

        return jsonify({'requests' : edit_request})


    @app.route('/api/v1/user/requests/<int:id>', methods=['DELETE'])
    @jwt_required
    def api_request_deleted(id):
        delete_request = [request for request in requests if request['id'] == id]
        print(len(delete_request))
        if len(delete_request) == 0:
            abort(404)
        requests.remove(delete_request[0])

        return jsonify({'requests' : requests})

    @app.route('/api/v1/auth/signout/', methods=['POST'])
    @jwt_required
    def signout():
        return jsonify({'message': 'Logged out successfully!'})

    return app