
class Api_Request(object):
    """This class represents the requests in Maintenance Tracker."""
    api_request =[{'id': 1, 
    'name': 'Computer Monitor', 
    'description': 'Broken screen', 
    'category': 'repair', 
    'department': 'Finance'
    }, {
        'id' : 2,
        'name': 'Server',
        'description': 'infected wit computer virus',
        'category': 'maintenance',
        'department': 'IT'
    }, {
        'id': 3,
        'name': 'Keyboard',
        'desription': 'Poured coffee on it',
        'category': 'repair',
        'department' : 'Accounts'
    }]


    def __init__(self):
        self.results = {}

    def create_request(self, id, name, description, category, department):
        if id == '' or name == '' or description == '' or category == '' or department == '':
            return "Please Fill in request details!"
        request2 = [request1 for request1 in Api_Request().api_request if request1['id'] == id]
        if request2:
            return "Request ID not found!"

        self.results['id'] = id
        self.results['name'] = name
        self.results['description'] = description
        self.results['category'] = category
        self.results['department'] = department
        Api_Request().append(self.results)
        return "Request created!"

    def view_all_requests(self):
        return Api_Request.api_request

    def view_single_request(self, id):
        request1 = [request1 for request1 in Api_Request().api_request if request1['id'] == id]
        if not request1:
            return 'Request not found!'
        return 'Request found!'

    def modify_request(self, id, new_request):
        request1 = [request1 for request1 in Api_Request().api_request if request1['id'] == id]
        if not request1:
            return 'Sorry, Request not found!'
        mod_request = request1[0]
        mod_request['name'] = new_request
        return 'Request modified!'

    def delete_request(self, id):
        request1 = [request1 for request1 in Api_Request().api_request if request1['id'] == id]
        if not request1:
            return 'Sorry, Request not found!'
        Api_Request.api_request.remove(request1[0])
        return 'Request deleted!'
