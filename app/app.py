from flask_api import FlaskAPI
from flask import request, jsonify, abort, make_response, json
from flask_jwt_extended import (jwt_required, create_access_token, get_jwt_identity, get_raw_jwt)
from functools import wraps
from passlib.hash import sha256_crypt
from flask_jwt_extended import JWTManager
from app.helpers import insert_user, get_user, create_request, get_requests, get_request, edit_request, delete_request, admin_get_requests, admin_modify_request
from app.models import User, Requests



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
            if user['username'] != 'admin':
                return jsonify({'message': 'Not authorized!'}), 401
            return f(*args, **kwargs)
        return wrapped



    @app.route('/api/v2/auth/signup/', methods=['POST'])
    def signup_user():
        user = User(name = request.json.get("name"),
                    email = request.json.get("email"),
                    username = request.json.get("username"),
                    password = sha256_crypt.encrypt(str(request.json.get("password"))),
                    role = request.json.get("role"))
        user.save()
        return jsonify({'message': 'New user registered!', 'User': user.__dict__})
        if user == "./?%$#@!*&":
            return jsonify({'message': 'User credentials required to register!'})



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
        return make_response('Could not verify!, Please Register!'), 401


    @app.route('/api/v2/auth/users/requests/', methods=['POST'])
    @jwt_required
    def api_request():

        username = get_jwt_identity()
        user = get_user(username)

        requests = Requests(name = request.json.get("name"), 
                            description = request.json.get("description"),
                            category = request.json.get("category"), 
                            department = request.json.get("department"),
                            user_id = (user["id"]))
        requests.save()
        return jsonify({'Requests' : requests.__dict__}), 201
        if requests == '':
            max_length = 70
            min_length = 10
            
            return jsonify({'message': 'Can not enter empty field!'})
        
        
    @app.route('/api/v2/auth/users/requests/', methods=['GET']) 
    @jwt_required
    def view_all_requests():
        username = get_jwt_identity()
        user = get_user(username)

        requests = get_requests(user['id'])
        if requests is None:
            return jsonify({'message': "Request not found!"})

        return jsonify({'request': requests})
        

    @app.route('/api/v2/auth/users/requests/<int:id>', methods=['GET'])
    @jwt_required
    def single_api_request(id):
        username = get_jwt_identity()
        user = get_user(username)
        # retrieve a request using it's ID

        requests = get_request(id)
        if requests is None:
            return jsonify({'message': "Request not found!"})

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
        if requests is None:
            return jsonify({'message': 'No requests found!'})
        return jsonify({'Requests': requests})

    @app.route('/api/v2/auth/requests/<int:id>', methods=['PUT'])
    @jwt_required
    @admin_required
    def admin_can_edit(id):
        username = get_jwt_identity()
        user = get_user(username)

        modify = get_request(id)

        if modify is None:
            return jsonify({'message': 'Request Not found!'})
        
        modify['status'] = request.json.get('status')
        print(modify)
        admin_modify_request(id, modify)
        
        return jsonify({'Requests': modify})
        

    @app.route('/api/v2/auth/signout/', methods=['POST'])
    @jwt_required
    def signout():
        return jsonify({'message': 'Logged out successfully!'})

    return app