import unittest
import os
import json
import app
import unittest
import json
from app.models import Api_Request

from app import create_app

class MaintenanceTrackerTestCase(unittest.TestCase):
    """This class represent user signup, signin, make request"""

    def setUp(self):
        """Define test variable and initialize app."""
        self.app = create_app(config_name="testing")
        self.checker = self.app.test_client()

    def test_create_request(self):
        """Test creating a request"""
        api_request = {"id": 1, "name": "Computer Monitor", "description": "Breken screen", "category": "repair", "department": "Finance"}
        response = self.checker.post(
            '/api/v1/requests/', data=json.dumps(api_request), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_view_single_request(self):
        """Test view a single request on API"""
        api_request = {"id": 2}
        response = self.checker.get(
            '/api/v1/requests/2', data=json.dumps(api_request), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_view_all_requests(self):
        """Test view all requests on the API"""
        response = self.checker.get(
            '/api/v1/requests/', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_modify_request(self):
        """Test modify a request on API"""
        api_request = {"id": 3, "name": "Keyboard", "description": "Pour coffee on it", "category": "repair", "department": "Accounts"}
        response = self.checker.put(
            '/api/v1/requests/3', data=json.dumps(api_request), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_request(self):
        """Test delete request"""
        api_request = {"id": 4}
        response = self.checker.delete(
            '/api/v1/requests/4', data=json.dumps(api_request), content_type='application/json')
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()