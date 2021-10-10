# Lambda Function for CoinBase

Install dependencies to the `package` directory

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

Upload to AWS
