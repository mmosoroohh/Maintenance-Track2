import unittest
import os
import json
import psycopg2
from flask.testing import FlaskClient


conn = psycopg2.connect("dbname='m_tracker_test' user='mmosoroohh' host='localhost' password='test123'")
cur = conn.cursor()

from app.app import create_app

class MaintenanceTrackerTestCase(unittest.TestCase):
    """This class represent user signup, signin, make request"""

    def setUp(self):
        """Define test variable and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.request = {'name': 'Computer Monitor', 'description': 'Broken screen', 'category': 'repair', 'department': 'Finance'}

        # bind the app to the current context
        with self.app.app_context():
            # create all tables
            cur.execute('''CREATE TABLE IF NOT EXISTS requests(id serial PRIMARY KEY, name varchar, description varchar, category varchar, department varchar, user_id INT REFERENCES(id));''')
            conn.commit()

        
    def test_create_request(self):
        """Test creating a request"""
        response = self.client.post(
            '/api/v2/requests/', data=json.dumps(self.request), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        assert isinstance(self, FlaskClient)

    def test_view_single_request(self):
        """Test view a single request on API"""
        response = self.client.get(
            '/api/v2/requests/1', data=json.dumps(self.request), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        assert isinstance(self, FlaskClient)

    def test_view_all_requests(self):
        """Test view all requests on the API"""
        response = self.client.get(
            '/api/v2/requests/', content_type='application/json')
        self.assertEqual(response.status_code, 200)
        assert isinstance(self, FlaskClient)

    def test_modify_request(self):
        """Test modify a request on API"""
        self.client.post('/api/v2/requests/', data=json.dumps(self.request), content_type='application/json')
        response = self.client.put('/api/v2/requests/1', data=json.dumps(self.request), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        assert isinstance(self, FlaskClient)

    def test_delete_request(self):
        """Test delete request"""
        response = self.client.get('/api/v2/requests/1', data=json.dumps(self.request), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.delete('/api/v2/requests/1',content_type='application/json')
        self.assertEqual(response.status_code, 404)
        assert isinstance(self, FlaskClient)

    def tearDown(self):
        """teardown all initialized variable"""
        with self.app.app_context():
            # drop all tables
            cur.execute("DROP TABLE IF EXITS requests")
            conn.commit()


if __name__ == "__main__":
    unittest.main()
