from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps

# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    from app.models import User, Requests


    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    db.init_app(app)



    @app.route('/api/v1/user', methods=['POST'])
    def create_user():
        data = request.get_json()

        hashed_password = generate_password_hash(data['password'], method='sha256')

        new_user = User(public_id=str(uuid.uuid4()), name=data['name'], email=data['email'], password=hashed_password, admin=False)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message' : 'New user created!'})

    @app.route('/api/v1/user', methods=['GET'])
    def get_all_users():

        users = User.query.all()

        output = []
        
        for user in users:
            user_data = {}
            user_data['public_id'] = user.public_id
            user_data['name'] = user.name
            user_data['email'] = user.email
            user_data['password'] = user.password
            user_data['admin'] = user.admin
            output.append(user_data)

        return jsonify({'users' : output})

    @app.route('/api/v1/user/<public_id>', methods=['GET'])
    def get_one_user(public_id):

        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({'message' : 'No user found!'})

        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['email'] = user.email
        user_data['password'] = user.password
        user_data['admin'] = user.admin

        return jsonify({'user' : user_data})

    @app.route('/api/v1/user/<public_id>', methods=['PUT'])
    def promote_user(public_id):

        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({'message' : 'No user found!'})

        user.admin = True
        db.session.commit()

        return jsonify({'message' : 'The user has been promoted!'})

    @app.route('/api/v1/user/<public_id>', methods=['DELETE'])
    def delete_user(public_id):

        user = User.query.filter_by(public_id=public_id).first()

        if not user:
            return jsonify({'message' : 'No user found!'})

        db.session.delete(user)
        db.session.commit()

        return jsonify({'message' : 'The user has been deleted!'})

    @app.route('/api/v1/login')
    def login():
        auth = request.authorization

        if not auth or not auth.username or auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

        user = User.query.filter_by(name=auth.username).first()

        if not user:
            return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

        if check_password_hash(user.password, auth.password):
            token = jwt.encode({'public_id' : user.public_id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET'])

            return jsonify({'token' : token.decode('UTF-8')})

        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})    


    @app.route('/api/v1/requests/', methods=['POST'])
    def create_request():
        name = str(request.data.get('name', ''))
        
        if name:
            request = Requests(name=name)
            request.save()
            response = jsonify({
                'id' : request.id,
                'name' : request.name,
                'description' : request.description,
                'category' : request.category,
                'department' : request.department
            })
            response.status_code = 201
            return response
        

    @app.route('/api/v1/requests/', methods=['GET'])
    def get_all_requests():
        requests = Requests.get_all_requests()
        results = []

        for request in requests:
            obj = {
                'id': request.id,
                'name': request.name,
                'description': request.description,
                'category': request.category,
                'department': request.department
            }
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response
        


    @app.route('/api/v1/requests/<int:id>', methods=['GET'])
    def get_one_request():
        # Retrieve a request using it's ID
        request = Requests.query.filter_by(id=id).first()
        if not request:
            # Raise an HTTPException with a 404 not found status code
            abort(404)

        else:
            response = jsonify({
                'id': request.id,
                'name': request.name,
                'description': request.description,
                'category': request.category,
                'department': request.department
            })
            response.status_code = 200
            return response
       

    
    @app.route('/api/v1/requests/<int:id>', methods=['PUT'])
    def modify_request():
        # retrieve a request by it's ID

        request = Requests.query.filter_by(id=id).first()
        if not request:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
        else:
            name = str(request.data.get('name', ''))
            request.name = name
            request.save()
            response = jsonify({
                'id': request.id,
                'name': request.name,
                'description': request.description,
                'category': request.category,
                'department': request.department
            })
            response.status_code = 200
            return response
        


    @app.route('/api/v1/requests/<int:id>', methods=['DELETE'])
    def delete_request():
        # retrieve a request using it's ID
        request = Requests.query.filter_by(id=id).first()
        if not request:
            # Raise an HTTPException with a 404 not found status code
            abort(404)
        else:
            request.delete()
            return {
                "message": "request {} deleted successfully".format(request.id)
        }, 200
        

            
    return app