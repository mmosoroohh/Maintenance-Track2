from app import helpers

class Requests(object):
    """This class represents the requests in Maintenance Tracker."""
   
    def __init__(self, id, name, description, category, department):
        self.id = id
        self.name = name
        self.description = description
        self.category = category
        self.department = department

class User(object):
    """This class represents the users for Maintenane Tracker."""

    ROLE_ADMIN = 1
    ROLE_NORMAL_USER = 2

    def __init__(self, id=0, name="", email="", username="", password="", role=""):
        self.id = id
        self.name = name
        self.email = email
        self.username = username
        self.password = password
        self.role = role

    def save(self):
        helpers.insert_user(self)
