import cbpro, os
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

weights = {'SOL-USD': Decimal('0.5'), 'ETH-USD': Decimal('0.5')}
money = Decimal('75.00')

API_KEY = os.getenv("API_KEY")
API_PASS = os.getenv("API_PASS")
API_SECRET = os.getenv("API_SECRET")

auth_client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASS)

SENDER = "Jerry Peng <jpeng@posteo.net>"
RECIPIENT = "jpeng@posteo.net"
AWS_REGION = "us-east-2"
CHARSET = "utf-8"
client = boto3.client('ses', region_name=AWS_REGION)

def send_email(subject, body):
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = SENDER
    msg['To'] = RECIPIENT

    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(body.encode(CHARSET), 'plain', CHARSET)
    msg_body.attach(textpart)

    try:
        response = client.send_raw_email(
            Source=SENDER,
            Destinations=[
                RECIPIENT
            ],
            RawMessage={
                'Data':msg.as_string(),
            }
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

def dca():
    for coin in weights:
        response = auth_client.place_market_order(
            product_id=coin,
            side='buy',
            funds=str(weights[coin] * money)
        )
        if "message" in response and response["message"] == "Insufficient funds":
            send_email("Insufficient Funds", "Deposit more money into CoinBase")
            return
    send_email("Successful CoinBase purchase", "Bought $SOL and $ETH")

def lambda_handler(event, lambda_context):
    dca()
