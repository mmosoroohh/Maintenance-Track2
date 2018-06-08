import unittest
import os
import json
import psycopg2
from flask.testing import FlaskClient

conn = psycopg2.connect("dbname='m_tracker_test' user='mmosoroohh' host='localhost' password='test123'")
cur = conn.cursor()


from app.app import create_app


class UserTestCase(unittest.TestCase):
    """This class represets user test case."""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.user = {'name': 'Arnold Osoro', 'email': 'arnoldmaengwe@gmail.com', 'username': 'Osoro', 'password': 'secret123'}

        # bind the app to current context
        with self.app.app_context():
            # create all tables
            cur.execute('''CREATE TABLE IF NOT EXISTS users(id serial PRIMARY KEY, name varchar, email varchar, username varchar, password varchar);''')
            conn.commit()
    
    def test_signup_user(self):
        """Test API can register a user (POST request)"""
        response = self.client().post('/api/v2/auth/signup/', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        assert isinstance(self, FlaskClient)

    def test_signup_username_exists(self):
        """Test API can register with existing username (POST request)."""
        res = self.client().post('api/v2/auth/signin/', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        assert isinstance(self, FlaskClient)

    def test_login_successful(self):
        res = self.client().post('/api/v1/auth/login/', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        assert isinstance(self, FlaskClient)
        

    def test_login_wrong_username(self):
        res = self.client().post(
            '/api/v2/auth/signin/',
            data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(res.status_code, 401)
        assert isinstance(self, FlaskClient)
    
    def test_login_wrong_password(self):
        res = self.client().post(
            '/api/v2/auth/signin/', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(res.status_code, 401)
        assert isinstance(self, FlaskClient)

    def test_logout_successful(self):
        res = self.client().post(
            '/api/v2/auth/signout/', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        assert isinstance(self, FlaskClient)


    def tearDown(self):
        """teardown all initialized variable"""
        with self.app.app_context():
            # drop all tables
            cur.execute("DROP TABLE IF EXISTS users")
            conn.commit()
            

# Make the test conveniently executable
if __name__ == "__main__":
    unittest.main()