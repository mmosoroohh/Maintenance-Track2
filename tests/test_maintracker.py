from tests import app
import unittest
import os
import json


from app import create_app, db

class MaintenanceTrackerTestCase(unittest.TestCase):
    """This class represent user signup, signin, make request"""

    def setUp(self):
        """Define test variable and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {
            "name": "Arnold Osoro",
            "email": "arnoldmaengwe@gmail.com",
            "password": "secret123"
        }
        self.new_request = {
            "name": "Computer monitor",
            "description": "Broken screen needs repair",
            "category": "repair",
            "department" : "Accounts"
        }

        # bind the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def register_user(self):
        """Register new user"""
        res = self.app.post('/api/v1/auth/signup',
        data = json.dumps(self.user),
        headers = {'content-type': "application/json"})
        return res

    def login_user(self):
        """Sign in account."""
        res = self.app.post('/api/v1/auth/signin',
        data = json.dumps(self.user),
        headers = {'content-type': "application/json"})
        return res

    def logout(self):
        """Log out of account"""
        return self.app.get('/api/v1/auth/logout', follow_redirects=True)

    def new_request(self):
        """ Create a new request."""
        res = self.app.post('/api/v1/dashboard/user<id>/new_request/',
        data = json.dumps(self.new_request),
        headers = {'content-type': "application/json"})
        return res

    def tearDown(self):
        """teardown all initialized variables"""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()