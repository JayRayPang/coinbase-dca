#!/usr/bin/python3

import cbpro, os
from dotenv import load_dotenv
from decimal import Decimal

load_dotenv()

weights = {'SOL-USD': Decimal('0.5'), 'ETH-USD': Decimal('0.5')}
money = Decimal('75.00')

API_KEY = os.getenv("API_KEY")
API_PASS = os.getenv("API_PASS")
API_SECRET = os.getenv("API_SECRET")
USD_ACCOUNT = os.getenv("USD_ACCOUNT")

auth_client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASS)

def dca():
    for coin in weights:
        response = auth_client.place_market_order(
            product_id=coin,
            side='buy',
            funds=str(weights[coin] * money)
        )
        print(response)

if __name__ == '__main__':
    dca()
