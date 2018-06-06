import unittest
import os
import json


from app.app import create_app


class UserTestCase(unittest.TestCase):
    """This class represets user test case."""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client()
        self.user = {'name': 'Arnold Osoro', 'email': 'arnoldmaengwe@gmail.com', 'username': 'Osoro', 'password': 'secret123'}
    
    def test_signup_user(self):
        """Test API can register a user (POST request)"""
        response = self.client().post('/api/v1/auth/signup/', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_signup_email_exists(self):
        """Test API can register with existing email (POST request)."""
        res = self.client().post('api/v1/auth/signin/', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/auth/signup/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('arnoldmaengwe@gmail.com', str(res.data))

    def test_login_successful(self):
        res = self.client().post('/api/v1/auth/login/', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        

    def test_login_wrong_email(self):
        res = self.client().post(
            '/api/v1/auth/signin/',
            data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(res.status_code, 401)
    
    def test_login_wrong_password(self):
        res = self.client().post(
            '/api/v1/auth/signin/', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(res.status_code, 401)

    def test_logout_successful(self):
        res = self.client().post(
            '/api/v1/auth/signout/', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(res.status_code, 200)




# Make the test conveniently executable
if __name__ == "__main__":
    unittest.main()