from typing import List
from flask import Blueprint
from flask import jsonify
from flask import request
from src import db
from src.models import User
from src.schemas.auth import validate_signup_json
from src.schemas.auth import validate_login_json
from flask_jwt_extended import create_access_token
auth_blueprint = Blueprint('auth_blueprint', __name__)


"""
Request Body: Object with user's name, email and password
Response: Message and status code determining if user could sign up or not
Description: Used to register an user
"""


@auth_blueprint.route('/sign-up', methods=['POST'])
def sign_up():
    validate_data = request.get_json()
    request_data = validate_signup_json(validate_data)

    # Check if request had the appropriate body format
    if not request_data['valid']:
        return jsonify({
            'message': 'Missing parameter'
        }), 400

    # Check if there is already a user registered with this e-mail
    user_data = request_data['user']
    is_registered = User.query.filter_by(email=user_data['email']).first()

    if is_registered is not None:
        return jsonify({
            'message': 'User already registered!'
        }), 400

    # Register user after passing through fail-safes
    sign_up_data = User(email=user_data['email'],
                        username=user_data['username'],
                        password=user_data['password'])

    if sign_up_data is not None:
        try:
            db.session.add(sign_up_data)
            db.session.commit()
        except Exception as e:
            return jsonify({
                'message': 'Error in database, try again!'
            }), 400

        return jsonify({
            'message': 'User registered successfully!'
        }), 200
    else:
        return jsonify({
            'message': 'Could not register user, try again!'
        }), 400

"""
Request Body: Object with user's email and password
Response: JWT Token and Status Code of request
Description: Used to allow user to access system
"""


@auth_blueprint.route('/login', methods=['POST'])
def login():
    validate_data = request.get_json()
    request_data = validate_login_json(validate_data)

    # Check if request had the appropriate body format
    if not request_data['valid']:
        return jsonify({
            'message': 'Missing parameter.'
        }), 400

    # Check if user is registered
    user_data = request_data['user']
    registered_user = User.query.filter_by(email=user_data['email']).first()

    if registered_user is None:
        return jsonify({
            'message': 'User not registered'
        }), 400

    # Check user credentials
    if user_data['password'] != registered_user.password:
        return jsonify({
            'message': 'Invalid Password'
        }), 400

    try:
        jwt_token = create_access_token(identity=user_data)
    except Exception as e:
        return jsonify({
            'message': 'Could not generate login token'
        }), 400

    return jsonify({
        'message': 'Logged in sucessfully',
        'JWT_Token': jwt_token
    }), 200


"""
Request Body: None
Response: Status code determining if content of users table was deleted
Description: Used to delete all entries in users table
"""


@auth_blueprint.route('/delete', methods=['DELETE'])
def delete():
    user_data = User.query.order_by(User.username).all()

    if len(user_data) >= 1:
        try:
            for user in user_data:
                db.session.delete(user)
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
