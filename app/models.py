
class Api_Request(object):
    """This class represents the requests in Maintenance Tracker."""
   

    def __init__(self, name, description, category, department):
        self.name = name
        self.description = description
        self.category = category
        self.department = department

