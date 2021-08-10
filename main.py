#!/usr/bin/python3

import cbpro, os
from dotenv import load_dotenv
from decimal import Decimal, ROUND_DOWN, ROUND_UP

load_dotenv()

weights = {'SOL-USD': Decimal('0.5'), 'ETH-USD': Decimal('0.5')}
money = Decimal('75.00')
multipliers = [ Decimal('0.995'), Decimal('0.985'), Decimal('0.975') ]

API_KEY = os.getenv("API_KEY")
API_PASS = os.getenv("API_PASS")
API_SECRET = os.getenv("API_SECRET")
USD_ACCOUNT = os.getenv("USD_ACCOUNT")

auth_client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASS)

def dca():
    for coin in weights:
        price = Decimal(auth_client.get_product_ticker(coin)['price'])
        for multiplier in multipliers:
            limit_price = (multiplier * price).quantize(Decimal('0.001'), ROUND_DOWN)
            limit_size = ((money * weights[coin]) / (limit_price * len(multipliers))).quantize(Decimal('0.001'), ROUND_DOWN)
            # For cryptocurrencies with a larger market price, CoinBase Pro API has a lower precision for their prices
            # and a higher precision for the size you can order
            if (price + 1).log10().quantize(Decimal('1'), ROUND_UP) >= 4:
                limit_price = (multiplier * price).quantize(Decimal('0.01'), ROUND_DOWN)
                limit_size = ((money * weights[coin]) / (limit_price * len(multipliers))).quantize(Decimal('0.00000001'), ROUND_DOWN)
            response = auth_client.place_limit_order(product_id=coin,
                side='buy',
                price=str(limit_price),
                size=str(limit_size)
            )
            print(response)
            if 'message' in response and response['message'] == 'Insufficient funds':
                balance = Decimal(auth_client.get_account(USD_ACCOUNT)['available'])
                if balance >= Decimal('5.00'):
                    print('Using remaining funds to buy')
                    limit_size = ((balance * weights[coin]) / limit_price).quantize(Decimal('0.01'), ROUND_DOWN)
                    if price.log10().quantize(Decimal('1'), ROUND_UP) >= 4:
                        limit_size = ((balance * weights[coin]) / limit_price).quantize(Decimal('0.00000001'), ROUND_DOWN)
                        print(auth_client.place_limit_order(product_id=coin,
                                    side='buy',
                                    price=str(limit_price),
                                    size=str(limit_size)))
                        break;

if __name__ == '__main__':
    dca()
