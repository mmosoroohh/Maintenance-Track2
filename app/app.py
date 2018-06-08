from flask_api import FlaskAPI
from flask import request, jsonify, abort, make_response
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity, get_raw_jwt)
from functools import wraps
from flask_jwt_extended import JWTManager
from app.helpers import insert_user, create_request, get_requests, get_user, get_request, edit_request, delete_request, admin_get_requests, admin_modify_request
from app.models import User



# local import
from instance.config import app_config


def create_app(config_name):


    app = FlaskAPI(__name__, instance_relative_config=True)

    app.config.from_object(app_config[config_name])
    

    jwt = JWTManager(app)


    def admin_required(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            user = get_user(get_jwt_identity())
            if user['role'] != 1:
                return jsonify({'message': 'Not authorized!'}), 401
            return f(*args, **kwargs)
        return wrapped



    @app.route('/api/v2/auth/signup/', methods=['POST'])
    def signup_user():
        user = User(name = request.json.get("name"),
                    email = request.json.get("email"),
                    username = request.json.get("username"),
                    password = request.json.get("password"))
        user.save()
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


    @app.route('/api/v2/auth/users/requests/', methods=['POST'])
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
        if requests['name'] == '':
            return jsonify({'message': 'Can not enter empty field!'})
        create_request(requests)
        return jsonify({'Requests' : requests}), 201
        
    @app.route('/api/v2/auth/users/requests/', methods=['GET']) 
    @jwt_required
    def view_all_requests():
        username = get_jwt_identity()
        user = get_user(username)
        
        requests = get_requests(user['id'])
        return jsonify({'request': requests})

    @app.route('/api/v2/auth/users/requests/<int:id>', methods=['GET'])
    @jwt_required
    def single_api_request(id):
        username = get_jwt_identity()
        user = get_user(username)
        # retrieve a request using it's ID

        requests = get_request(id)
        return jsonify({'request': requests})

    @app.route('/api/v2/auth/users/requests/<int:id>', methods=['PUT'])
    @jwt_required
    def api_request_modified(id):
        username = get_jwt_identity()
        user = get_user(username)
        # retrieve a request using it's ID
        edit = get_request(id)
        
        if edit is None:
            return jsonify({'message': 'Request not found!'})

        edit['name']= request.json.get('name')
        edit['description'] = request.json.get('description')
        edit['category']= request.json.get('category')
        edit['department']=request.json.get('department')
    
        edit_request(id, edit)

        return jsonify({'requests' : edit})


    @app.route('/api/v2/auth/users/requests/<int:id>', methods=['DELETE'])
    @jwt_required
    def api_request_deleted(id):
        username = get_jwt_identity()
        user = get_user(username)

        requests = get_request(id)
        if requests is None:
            return jsonify({'message': "Request not found!"})
        
        delete_request(id)
        return jsonify({'message' : 'Request has been deleted!'})

    @app.route('/api/v2/auth/requests/', methods=['GET'])
    @jwt_required
    @admin_required
    def admi_get_all_requests():
        username = get_jwt_identity()
        user = get_user(username)

        requests = admin_get_requests()
        return jsonify({'message': requests})

    @app.route('/api/v2/auth/requests/<int:id>', methods=['PUT'])
    @jwt_required
    @admin_required
    def admin_can_modify(id):
        username = get_jwt_identity()
        user = get_user(username)

        modify = get_request(id)

        if modify is None:
            return jsonify({'message': 'Request Not found!'})
        
        modify['status'] = request.json.get('status')

        admin_can_modify(modify)

        return jsonify({'Requests': modify})


    @app.route('/api/v2/auth/signout/', methods=['POST'])
    @jwt_required
    def signout():
        return jsonify({'message': 'Logged out successfully!'})

    return app