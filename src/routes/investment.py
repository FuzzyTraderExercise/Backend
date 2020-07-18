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
from flask_jwt_extended import jwt_required
investment_blueprint = Blueprint('investment_blueprint', __name__)

"""
Request Args: USD Value for how much user can spend on investment
Response: List of investments
Description: Returns a list of investments with value equal or below
value sent by user
"""


@investment_blueprint.route('/get-investments', methods=['GET'])
@jwt_required
def get_investments():
    usd_value = request.args.get('usd_value')

    if usd_value is None:
        return jsonify({
            'message': 'Missing usd_value parameter'
        }), 400

    query = Investment.query.filter(Investment.usd_value <= usd_value).all()

    if len(query) < 1:
        return jsonify({
            'Message': 'There is no stock that fits your value range'
        }), 400

    count = 0
    stock_list = []
    for stock in query:
        temp_stock = {
            'name': stock.stock_name,
            'usd_value': stock.usd_value,
            'bitcoin_value': stock.bitcoin_value,
            'is_bitcoin': stock.is_bitcoin
        }

        stock_list.append(temp_stock)

    return jsonify({
        'stocks': stock_list,
    }), 200


"""
Request Args: None
Response: Status code to determine success or not
Description: Connect to Market Stack API and populate db
"""


@investment_blueprint.route('/populate-market-share', methods=['POST'])
def post_market_share():
    url = 'http://api.marketstack.com/v1/eod'
    symbols = 'AAPL,MSFT,AMZN,GOOGL,FB,BABA,TCEHY,BRK/B,V,JNJ, \
                WMT,TV,TSM,,NSRGY,NSRGF,PG,RHHBY,MA,RHHVF,JPM, \
                UNH,TSLA,HD,INTC,NVDA,LVMUY,NFLX,IDCBF,VZ'

    params = {
        'access_key': os.getenv('MARKET_STACK_KEY'),
        'symbols': symbols,
        'date_from': '2020-07-16',
        'date_to': '2020-07-16'
    }

    response = requests.get(url, params=params)

    if response.status_code == 400:
        return jsonify({
            'message': 'Could not connect to response api'
        }), 400

    response = response.json()

    for stock_data in response['data']:
        stock = Investment(stock_name=stock_data['symbol'],
                           usd_value=stock_data['close'],
                           is_bitcoin=False)

        try:
            db.session.add(stock)
            db.session.commit()
        except Exception as e:
            return jsonify({
                'message': 'Could not populate database'
            }), 400

    return jsonify({
        'message': 'Database populated successfully'
    }), 200


"""
Request Body: None
Response: Status code to determine success or not
Description: Connect to blockchain api and populate db
"""


@investment_blueprint.route('/populate-bitcoin', methods=['POST'])
def post_bitcoin():
    url = 'https://blockchain.info/tobtc'
    params = {
        'currency': 'USD',
        'value': 500,
        'cors': 'TRUE'
    }

    response = requests.get(url, params=params)

    if response.status_code == 400:
        return jsonify({
            'message': 'Could not connect to blockchain API'
        }), 400

    response = response.json()
    bitcoin = Investment(stock_name='Bitcoin',
                         usd_value=500,
                         is_bitcoin=True,
                         bitcoin_value=response)

    try:
        db.session.add(bitcoin)
        db.session.commit()
    except Exception as e:
        return jsonify({
            'Message': 'Could not store bitcoin in database'
        }), 400

    return jsonify({
        'Message': 'Stored bitcoin sucessfully'
    }), 200


"""
Request Body: None
Response: Status code determining if content of investments table was deleted
Description: Used to delete all entries in investments table
"""


@investment_blueprint.route('/delete-investments', methods=['DELETE'])
def delete():
    query = Investment.query.order_by(Investment.stock_name).all()

    if len(query) >= 1:
        try:
            for stock in query:
                db.session.delete(stock)
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
