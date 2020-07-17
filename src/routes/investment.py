import os
import requests
import sys
from typing import List
from flask import Blueprint
from flask import jsonify
from flask import request
from src import db
from src.models import Investment
investment_blueprint = Blueprint('investment_blueprint', __name__)

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
