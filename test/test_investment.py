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
        self.app.delete('/delete')
        self.app.delete('/delete-investments')

    """
    Commented because using it repeatedly could exaust api's free trial
    def test_should_populate_database_with_stock(self):
        response = self.app.post('/populate-market-share')
        self.assertEqual(response.status_code, 200)
    """

    def test_should_populate_database_with_bitcoin(self):
        response = self.app.post('/populate-bitcoin')
        self.assertEqual(response.status_code, 200)

    def test_should_get_stocks_below_usd_value(self):
        # Get JWT Token and populate investments table
        JWT_TOKEN = signup_and_login(self.app)
        self.app.post('/populate-bitcoin')

        headers = {
            'Authorization': 'Bearer ' + JWT_TOKEN
        }

        params = {
            'usd_value': 500
        }

        response = self.app.get('/get-investments', headers=headers, query_string=params)
        self.assertEqual(response.status_code, 200)

    def test_should_not_get_stocks_if_there_are_none(self):
        # Get JWT Token
        JWT_TOKEN = signup_and_login(self.app)

        headers = {
            'Authorization': 'Bearer ' + JWT_TOKEN
        }

        params = {
            'usd_value': 500
        }

        response = self.app.get('/get-investments', headers=headers, query_string=params)
        self.assertEqual(response.status_code, 400)

    def test_should_not_get_stocks_without_jwt_token(self):
        params = {
            'usd_value': 500
        }

        response = self.app.get('/get-investments', query_string=params)
        self.assertEqual(response.status_code, 401)

    def test_should_not_get_stocks_without_usd_value(self):
        JWT_TOKEN = signup_and_login(self.app)

        headers = {
            'Authorization': 'Bearer ' + JWT_TOKEN
        }

        response = self.app.get('/get-investments', headers=headers)
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
