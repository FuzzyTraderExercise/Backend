import os
import requests
import json
import sys
from typing import List
from flask import Blueprint
from flask import jsonify
from flask import request
from src import db
from src.models import Investment
from src.models import User
from src.models import UserInvestment
from src.schemas.user_investment import validate_user_investment_json
from flask_jwt_extended import jwt_required
user_investment_blueprint = Blueprint('user_investment_blueprint',
                                      __name__)


"""
Request Body: User email and investment name
Response: Status Code
Description: Registers an investment bought by user
"""


@user_investment_blueprint.route('/register-investment', methods=['POST'])
@jwt_required
def register_user_investment():
    validate_data = request.get_json()
    request_data = validate_user_investment_json(validate_data)

    # Check if request had the appropriate body format
    if not request_data['valid']:
        return jsonify({
            'message': 'Missing parameter'
        }), 400

    user_email = request_data['register']['email']
    stock_name = request_data['register']['stock_name']
    user = User.query.filter_by(email=user_email).first()
    stock = Investment.query.filter_by(stock_name=stock_name).first()

    if user is None or stock is None:
        return jsonify({
            'message': 'Invalid data'
        }), 400

    # Check if user already bought this stock before
    user_investment = UserInvestment.query.filter_by(investment_id=stock.id,
                                                     user_id=user.id).first()

    if user_investment is None:
        user_investment = UserInvestment(user_id=user.id,
                                         investment_id=stock.id,
                                         usd_value=stock.usd_value)
    else:
        user_investment.usd_value += stock.usd_value

    try:
        db.session.add(user_investment)
        db.session.commit()
    except Exception as e:
        return jsonify({
            'message': 'Error connecting to database'
        }), 400

    return jsonify({
        'message': 'User investment registered sucessfully'
    }), 200


"""
Request Body: None
Response: Status Code
Description: Deletes all entries in user investments table
"""


@user_investment_blueprint.route('/delete-userinvestment', methods=['DELETE'])
def delete_user_investment():
    query = UserInvestment.query.order_by(UserInvestment.usd_value).all()

    if len(query) >= 1:
        try:
            for user_investment in query:
                db.session.delete(user_investment)
            db.session.commit()
        except Exception as e:
            return jsonify({
                'message': 'Error in database, try again!'
            }), 400

        return jsonify({
            'message': 'Records sucessfully deleted'
        }), 200
    else:
        return jsonify({
            'message': 'No records to delete'
        }), 400
