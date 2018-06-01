from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort



# local import
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):
    from app.models import Api_Request


    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
    db.init_app(app)



    @app.route('/api/v1/requests/', methods=['POST', 'GET'])
    def api_request():
        if request.method == "POST":

            data = request.get_json()

            if data:
                api_request = Api_Request(name=data['name'], description=data['description'], category=data['category'], department=data['department'])
                api_request.save()
                response = jsonify({
                    'id': api_request.id,
                    'name': api_request.name,
                    'description': api_request.description,
                    'category': api_request.category,
                    'department': api_request.department
                })
                response.status_code = 201
                return jsonify({'message' : 'New request created!'})
        else:
            # GET
            api_requests = Api_Request.get_all()
            results = []

            for api_request in api_requests:
                obj = {
                    'id': api_request.id,
                    'name': api_request.name,
                    'description': api_request.description,
                    'category': api_request.category,
                    'department': api_request.department
                }
                results.append(obj)
            response = jsonify(results)
            response.status_code = 200
            return response


    @app.route('/api/v1/requests/<int:id>', methods=['GET'])
    def single_api_request(id):
        # retrieve a request using it's ID
        api_request = Api_Request.query.filter_by(id=id).first()
        if  not api_request:
            return jsonify({'message': 'No request found!'})

        obj = {
            'id': api_request.id,
            'name': api_request.name,
            'description': api_request.description,
            'category': api_request.category,
            'department': api_request.department
        }

        return jsonify({'api_request': obj})

    @app.route('/api/v1/requests/<int:id>', methods=['PUT'])
    def api_request_modified(id):
        api_request = Api_Request.query.filter_by(id=id).first() 

        if not api_request:
            return jsonify({'message' : 'No request found!'})
        
        else:
            data = request.get_json()
            api_request = Api_Request(name=data['name'], description=data['description'], category=data['category'], department=data['department'])
            api_request.save()
            response = jsonify({
                'id': api_request.id,
                'name': api_request.name,
                'description': api_request.description,
                'category': api_request.category,
                'department': api_request.department
            })
            response.status_code = 201
            return jsonify({'message' : 'Request has been modified!'})


    @app.route('/api/v1/requests/<int:id>', methods=['DELETE'])
    def api_request_deleted(id):
        api_request = Api_Request.query.filter_by(id=id).first()
        
        if not api_request:
            return jsonify({'message': 'No request found!'})

        api_request.delete()
        return jsonify({'message' : 'Request has been deleted!'})

    return app