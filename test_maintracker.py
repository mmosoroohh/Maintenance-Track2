import unittest
import os
import json


from app import create_app

class MaintenanceTrackerTestCase(unittest.TestCase):
    """This class represent Maintenance Tracker requests test case"""

    def setUp(self):
        """Define test variable and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.api_request = {'name': 'Computer monitor','description': 'Broken screen needs repair', 'category': 'repair', 'department' : 'Accounts'}

        # bind the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_create_request(self):
        """Test API can create a request (POST request)"""
        res = self.client().post('/api/v1/requests/', data=self.api_request)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Computer monitor', str(res.data))

    def test_api_can_get_all_requests(self):
        """Test API can get a request (GET request)"""
        res = self.client().post('/api/v1/requests/', data=self.api_request)
        self.assertEqual(res.status_code, 201)
        res =self.client().get('/api/v1/requests/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Computer monitor', str(res.data))

    def test_api_can_get_request_by_id(self):
        """Test API can get a single request by using id."""
        rv = self.client().post('/api/v1/requests/', data=self.api_request)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result =self.client().get(
            '/api/v1/requests/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Computer monitor', str(result.data))

    def test_request_can_be_modified(self):
        """Test APi can modify existing request. (PUT request)"""
        rv = self.client().post(
            '/api/v1/requests/1',
            data={'name': 'Printer'})
        self.assertEqual(rv.status_code, 200)
        results =self.client().get('/api/v1/requests/1')
        self.assertIn('Printer', str(results.data))

    def test_delete_request(self):
        """Test Api can delete an existing request. (DELETE request)"""
        rv = self.client().post(
            '/api/v1/requests/',
            data={'name': 'Printer'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/api/v1/requests/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exits, should return a 404
        result = self.client().get('/api/v1/requests/1')
        self.assertEqual(result.status_code, 404)
  
    def tearDown(self):
        """teardown all initialized variables"""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

if __name__ == "__main__":
    unittest.main()