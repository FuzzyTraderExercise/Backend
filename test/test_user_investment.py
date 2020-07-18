import os
import unittest
import requests
import json
import sys
from flask import jsonify
from src import create_app, db
import config

 
app = create_app()

class InvestmentTests(unittest.TestCase):

    # Set up test environment
    def setUp(self):
        app.config['TESTING'] = True
        app.config['ENV'] = 'testing'
        app.config['DEBUG'] = False 
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL')
        self.app = app.test_client()
        self.app.testing = True

    # Delete users created in tests
    def tearDown(self):
        self.app.delete('delete-userinvestment')
        self.app.delete('/delete')
        self.app.delete('/delete-investments')

    def test_should_register_user_investment(self):
        # Get JWT Token and populate investments table
        JWT_TOKEN = signup_and_login(self.app)
        self.app.post('/populate-bitcoin')

        headers = {
            'Authorization': 'Bearer ' + JWT_TOKEN
        }

        payload = {
            'email': 'marina@gmail.com',
            'stock_name': 'Bitcoin' 
        }

        response = self.app.post('/register-investment',
                                 headers=headers,
                                 json=payload)
        self.assertEqual(response.status_code, 200)

    def test_should_not_register_user_investment_without_jwt_token(self):
        JWT_TOKEN = signup_and_login(self.app)
        self.app.post('/populate-bitcoin')

        payload = {
            'email': 'marina@gmail.com',
            'stock_name': 'Bitcoin' 
        }

        response = self.app.post('/register-investment',
                                 json=payload)
        self.assertEqual(response.status_code, 401)

    def test_should_not_register_user_investment_without_email(self):
        # Get JWT Token and populate investments table
        JWT_TOKEN = signup_and_login(self.app)
        self.app.post('/populate-bitcoin')

        headers = {
            'Authorization': 'Bearer ' + JWT_TOKEN
        }

        payload = {
            'stock_name': 'Bitcoin' 
        }

        response = self.app.post('/register-investment',
                                 headers=headers,
                                 json=payload)
        self.assertEqual(response.status_code, 400)

    def test_should_not_register_user_investment_without_stock(self):
        # Get JWT Token and populate investments table
        JWT_TOKEN = signup_and_login(self.app)
        self.app.post('/populate-bitcoin')

        headers = {
            'Authorization': 'Bearer ' + JWT_TOKEN
        }

        payload = {
            'email': 'marina@gmail.com' 
        }

        response = self.app.post('/register-investment',
                                 headers=headers,
                                 json=payload)
        self.assertEqual(response.status_code, 400)

    def test_should_not_register_user_investment_for_invalid_user(self):
        # Get JWT Token and populate investments table
        JWT_TOKEN = signup_and_login(self.app)
        self.app.post('/populate-bitcoin')

        headers = {
            'Authorization': 'Bearer ' + JWT_TOKEN
        }

        payload = {
            'email': 'invalido@gmail.com',
            'stock_name': 'Bitcoin' 
        }

        response = self.app.post('/register-investment',
                                 headers=headers,
                                 json=payload)
        self.assertEqual(response.status_code, 400)

    def test_should_not_register__user_investment_for_invalid_stock(self):
        # Get JWT Token and populate investments table
        JWT_TOKEN = signup_and_login(self.app)
        self.app.post('/populate-bitcoin')

        headers = {
            'Authorization': 'Bearer ' + JWT_TOKEN
        }

        payload = {
            'email': 'marina@gmail.com',
            'stock_name': 'Invalid' 
        }

        response = self.app.post('/register-investment',
                                 headers=headers,
                                 json=payload)
        self.assertEqual(response.status_code, 400)

# Sign up and log in to get JWT Token   
def signup_and_login(client):
    payload = {
        'username': 'marina',
        'email': 'marina@gmail.com',
        'password': 'senha123'
    }
    headers = {'content-type': 'application/json'}

    response = client.post('/sign-up', json=payload)
    response = client.post('/login', json=payload)

    return response.json['JWT_Token']

if __name__ == "__main__":
    unittest.main()
