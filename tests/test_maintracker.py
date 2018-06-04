import unittest
import os
import json


from app.app import create_app

class MaintenanceTrackerTestCase(unittest.TestCase):
    """This class represent user signup, signin, make request"""

    def setUp(self):
        """Define test variable and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.request = {'name': 'Computer Monitor', 'description': 'Broken screen', 'category': 'repair', 'department': 'Finance'}

    def test_create_request(self):
        """Test creating a request"""
        response = self.client.post(
            '/api/v1/requests/', data=json.dumps(self.request), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_view_single_request(self):
        """Test view a single request on API"""
        response = self.client.get(
            '/api/v1/requests/1', data=json.dumps(self.request), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_view_all_requests(self):
        """Test view all requests on the API"""
        response = self.client.get(
            '/api/v1/requests/', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_modify_request(self):
        """Test modify a request on API"""
        self.client.post('/api/v1/requests/', data=json.dumps(self.request), content_type='application/json')
        response = self.client.put('/api/v1/requests/1', data=json.dumps(self.request), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_request(self):
        """Test delete request"""
        response = self.client.get('/api/v1/requests/1', data=json.dumps(self.request), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.delete('/api/v1/requests/1',content_type='application/json')
        self.assertEqual(response.status_code, 404)



if __name__ == "__main__":
    unittest.main()
