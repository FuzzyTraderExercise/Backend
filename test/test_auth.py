import os
import unittest
import requests
import json
 
from src import create_app, db
import config

 
app = create_app()

class AuthTests(unittest.TestCase):

    # Set up test environment
    def setUp(self):
        app.config['TESTING'] = True
        app.config['ENV'] = 'testing'
        app.config['DEBUG'] = False 
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL')
        self.app = app.test_client()
        self.app.testing = True

    # Delete data in test database
    def tearDown(self):
        self.app.delete('/delete')

    # Sign up tests
    def test_should_signup(self):
        payload = {
            'username': 'marina',
            'email': 'marina@gmail.com',
            'password': 'senha123'
        }

        response = self.app.post('/sign-up', json=payload)
        self.assertEqual(response.status_code, 200)

    def test_should_not_signup_with_missing_username(self):
        payload = {
            'email': 'marina@gmail.com',
            'password': 'senha123'
        }

        response = self.app.post('/sign-up', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_should_not_signup_with_missing_email(self):
        payload = {
            'username': 'marina',
            'password': 'senha123'
        }

        response = self.app.post('/sign-up', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_should_not_signup_with_missing_password(self):
        payload = {
            'username': 'marina',
            'email': 'marina@gmail.com'
        }

        response = self.app.post('/sign-up', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_should_not_signup_with_repeated_email(self):
        payload = {
            'username': 'marina',
            'email': 'primeiro@gmail.com',
            'password': 'senha123'
        }

        # Try to register an user with the same e-mail twice
        response = self.app.post('/sign-up', json=payload)
        response = self.app.post('/sign-up', json=payload)
        self.assertEqual(response.status_code, 400)

    # Login Tests
    def test_should_login(self):
        payload = {
            'username': 'marina',
            'email': 'marina@gmail.com',
            'password': 'senha123'
        }

        response = self.app.post('/sign-up', json=payload)

        if response.status_code == 200:
            payload = {
            'email': 'marina@gmail.com',
            'password': 'senha123'
            }

            response = self.app.post('/login', json=payload)
            self.assertEqual(response.status_code, 200)
        else:
            assert(False)

    def test_should_not_login_with_wrong_password(self):
        payload = {
            'username': 'marina',
            'email': 'marina@gmail.com',
            'password': 'senha123'
        }

        response = self.app.post('/sign-up', json=payload)

        if response.status_code == 200:
            payload = {
            'email': 'marina@gmail.com',
            'password': 'senha1234'
            }

            response = self.app.post('/login', json=payload)
            self.assertEqual(response.status_code, 400)
        else:
            assert(False)

    def test_should_not_login_with_unregistered_user(self):
        payload = {
        'email': 'marina@gmail.com',
        'password': 'senha1234'
        }

        response = self.app.post('/login', json=payload)
        self.assertEqual(response.status_code, 400)

    def test_should_not_login_with_missing_email(self):
        payload = {
            'username': 'marina',
            'email': 'marina@gmail.com',
            'password': 'senha123'
        }

        response = self.app.post('/sign-up', json=payload)

        if response.status_code == 200:
            payload = {
            'password': 'senha123'
            }

            response = self.app.post('/login', json=payload)
            self.assertEqual(response.status_code, 400)
        else:
            assert(False)

    def test_should_not_login_with_missing_password(self):
        payload = {
            'username': 'marina',
            'email': 'marina@gmail.com',
            'password': 'senha123'
        }

        response = self.app.post('/sign-up', json=payload)

        if response.status_code == 200:
            payload = {
            'email': 'marina@gmail.com'
            }

            response = self.app.post('/login', json=payload)
            self.assertEqual(response.status_code, 400)
        else:
            assert(False)
    
    def test_should_delete_users(self):
        payload = {
            'username': 'marina',
            'email': 'deletar@gmail.com',
            'password': 'senha123'
        }

        response = self.app.post('/sign-up', json=payload)
        response = self.app.delete('/delete')
        self.assertEqual(response.status_code, 200)

    def test_should_not_delete_users_when_there_are_none(self):
        response = self.app.delete('/delete')
        self.assertEqual(response.status_code, 400)

if __name__ == "__main__":
    unittest.main()