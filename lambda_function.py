import cbpro
import os
import boto3
import json
from botocore.exceptions import ClientError
from decimal import Decimal
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

weights = {'SOL-USD': Decimal('0.5'), 'ETH-USD': Decimal('0.5')}
money = Decimal('75.00')

API_KEY = os.getenv("API_KEY")
API_PASS = os.getenv("API_PASS")
API_SECRET = os.getenv("API_SECRET")

auth_client = cbpro.AuthenticatedClient(API_KEY, API_SECRET, API_PASS)

SENDER = "Jerry Peng <jpeng@disroot.org>"
RECIPIENT = "jpeng@posteo.net"
AWS_REGION = "us-east-2"
CHARSET = "utf-8"
BODY_HTML = """\
<html>
<head></head>
<body>
<h1>BUY COINS</h1>
<p>%s</p>
</body>
</html>
"""
client = boto3.client('ses', region_name=AWS_REGION)

def send_email(subject, body):
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = SENDER
    msg['To'] = RECIPIENT

    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(body.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText((BODY_HTML % body).encode(CHARSET), 'html', CHARSET)
    msg_body.attach(textpart)
    msg_body.attach(htmlpart)
    msg.attach(msg_body)

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
    responses = []
    for coin in weights:
        response = auth_client.place_market_order(
            product_id=coin,
            side='buy',
            funds=str(weights[coin] * money)
        )
        if "message" in response and response["message"] == "Insufficient funds":
            if not responses:
                body = json.dumps(response, indent=4)
                send_email("Insufficient Funds", body)
            else:
                body = json.dumps(responses, indent=4)
                subject = "Insufficient Funds, made %d orders(s)" % len(responses)
                send_email(subject, body)
            return
        responses.append(response)
    body = json.dumps(responses, indent=4)
    send_email("Orders", body)

def lambda_handler(event, lambda_context):
    dca()
