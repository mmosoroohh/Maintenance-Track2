import unittest
import os
import json
from app import create_app, db


class UserTestCase(unittest.TestCase):
    """This class represets user test case."""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.user = {'name': 'Arnold Osoro', 'email': 'arnoldmaengwe@gmail.com', 'password': 'secret123'}

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    
    def test_create_user(self):
        """Test API can create a user (POST request)"""
        res = self.client().post('/users/', data=self.user)
        self.assertEqual(res.status_code, 201)
        self.assertIn('Arnold Osoro', str(res.data))

    def test_get_all_users(self):
        """Test API can get a user (GET request)."""
        res = self.client().post('/users/', data=self.user)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/users/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('Arnold Osoro', str(res.data))

    def test_get_user_by_id(self):
        """Test API can get a single user by using his/her id."""
        rv = self.client().post('/users/', data=self.user)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/users/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('Arnold Osoro', str(result.data))

    def test_delete_user(self):
        """Test API can delete an existing user. (DELETE request)."""
        rv = self.client().post(
            '/users/',
            data={'name': 'Brian Osoro', 'email': 'brian@gmail.com', 'password': 'brian123'})
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/users/1')
        self.assertEqual(res.status_code, 200)

        # Test to see if it exists, should return a 404
        result = self.client().get('/users/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

# Make the test conveniently executable
if __name__ == "__main__":
    unittest.main()