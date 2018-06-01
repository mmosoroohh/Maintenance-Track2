from flask_api import FlaskAPI
from flask import request, jsonify



# local import
from instance.config import app_config


def create_app(config_name):
    from app.models import Api_Request


    app = FlaskAPI(__name__, instance_relative_config=True)
    
    



    @app.route('/api/v1/requests/', methods=['POST'])
    def api_request():
        create_request = request.get_json(force=True)
        api_request = Api_Request.api_request(create_request['id'], create_request['name'], create_request['description'], create_request['category'], create_request['department'])

        return jsonify({'message' : 'New request created!'})
        
    @app.route('/api/v1/requests/', methods=['GET']) 
    def view_all_requests():
        requests = view_all_requests()
        return jsonify({'message': requests})

    @app.route('/api/v1/requests/<int:id>', methods=['GET'])
    def single_api_request(id):
        # retrieve a request using it's ID
        results = Api_Request.view_single_request(id)

        return jsonify({'message': results})

    @app.route('/api/v1/requests/<int:id>', methods=['PUT'])
    def api_request_modified(id):
        edit = request.get_json(force=True)
        modified = Api_Request.modified_request(
            edit['id'], edit['name'])
        return jsonify({'message' : 'Request has been modified!'})


    @app.route('/api/v1/requests/<int:id>', methods=['DELETE'])
    def api_request_deleted(id):
        delete = Api_Request.delete_request(id)

        return jsonify({'message' : 'Request has been deleted!'})

    return app