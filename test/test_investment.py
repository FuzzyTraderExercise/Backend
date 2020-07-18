import os
import unittest
import requests
import json
 
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

    def tearDown(self):
        pass

    """
    Commented because using it repeatedly could exaust api's free trial
    def test_should_populate_database_with_stock(self):
        response = self.app.post('/populate-market-share')
        self.assertEqual(response.status_code, 200)
    """

    def test_should_populate_database_with_bitcoin(self):
        response = self.app.post('/populate-bitcoin')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
