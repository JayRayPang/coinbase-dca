# Lambda Function for CoinBase

## Getting API Key from CoinBase

Sign in to CoinBase Pro and navigate to the [API Menu](https://pro.coinbase.com/profile/api).
Generate an API Key, and give it the permissions to for at least View and Trade.
Keep temporary note of the API Secret and Password because you will need them for the environment
variables in Lambda.

## Setting Up AWS Lambda

### Preparing .zip file for AWS Lambda

You will also want to first change the emails in the code.

First, install dependencies to the `package` directory

```
pip install --target ./package cbpro boto3
```

Create deployment package with installed dependencies at root

```
cd package
zip -r ../deployment-package.zip .
cd ..
zip -g deployment-package.zip lambda_function.py
```

Finally, upload the .zip to AWS Lambda and set the API\_KEY, API\_PASS, and API\_SECRET
environment variables in Lambda to what you got from CoinBase in the earlier steps. Note
that while Lambda will encrypt these, anybody who has access to the AWS Console will be
able to view your API Secrets in plaintext. If you want to follow best practices, you
should encrypt these with AWS KMS and decrypt it within the Lambda at runtime. KMS
does not have a free tier and will cost $1/month to create one key to do this. More
information about KMS pricing [here](https://aws.amazon.com/kms/pricing/).

### Set up a CloudWatch Event Rule

1. Go to CloudWatch in the AWS Console
2. Navigate to Events > Rules
3. Click 'Create rule' and set up a cron schedule with the lambda you just created
as a target. I use `10 4 * * ? *` for every day at 04:10 GMT

### Set up SES

Verify your emails in Simple Email Service, then add an IAM Role or Policy which allows
your Lambda to invoke SendRawEmail and SendEmail
