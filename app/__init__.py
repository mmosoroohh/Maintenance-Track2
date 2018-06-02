from flask_api import FlaskAPI
from flask import request, jsonify, abort



# local import
from instance.config import app_config


def create_app(config_name):


    app = FlaskAPI(__name__, instance_relative_config=True)
    
    requests = []

    @app.route('/api/v1/requests/', methods=['POST'])
    def api_request():

        add_request = {'id': len(requests)+1,
           'name': request.json.get('name'), 
           'description': request.json.get('description'),
            'category': request.json.get('category'), 
            'department': request.json.get('department')
        }
        requests.append(add_request)
        return jsonify({'Requests' : requests}), 201
        
    @app.route('/api/v1/requests/', methods=['GET']) 
    def view_all_requests():
        return jsonify({'request': requests})

    @app.route('/api/v1/requests/<int:id>', methods=['GET'])
    def single_api_request(id):
        # retrieve a request using it's ID
        single_request = [request for request in requests if request['id'] == id]

        return jsonify({'request': single_request})

    @app.route('/api/v1/requests/<int:id>', methods=['PUT'])
    def api_request_modified(id):
        edit_request = [request for request in requests if request['id'] == id]
        if len(edit_request) == 0:
            abort (404)
        edit_request = {
                'name': request.json.get('name'),
                'description': request.json.get('description'),
                'category': request.json.get('category'),
                'department': request.json.get('department')
            }
        return jsonify({'requests' : edit_request})


    @app.route('/api/v1/requests/<int:id>', methods=['DELETE'])
    def api_request_deleted(id):
        delete_request = [request for request in requests if request['id'] == id]
        print(len(delete_request))
        if len(delete_request) == 0:
            abort(404)
        requests.remove(delete_request[0])

        return jsonify({'requests' : requests})

    return app