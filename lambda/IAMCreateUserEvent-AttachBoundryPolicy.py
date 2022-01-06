import json
import boto3

def lambda_handler(event, context):
    
    account = event['account']
    iam_user = event['detail']['responseElements']['user']['userName']  

    sts_connection = boto3.client('sts')
    acct_b = sts_connection.assume_role(
        RoleArn="arn:aws:iam::" + account + ":role/Automation",
        RoleSessionName="cross_account_lambda"
    )
    
    ACCESS_KEY = acct_b['Credentials']['AccessKeyId']
    SECRET_KEY = acct_b['Credentials']['SecretAccessKey']
    SESSION_TOKEN = acct_b['Credentials']['SessionToken']

    # create service client using the assumed role credentials, e.g. S3
    client = boto3.client(
        'iam',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        aws_session_token=SESSION_TOKEN,
    )

    response = client.put_user_permissions_boundary(
    UserName=iam_user,
    PermissionsBoundary="arn:aws:iam::" + account + ":policy/PermissionsBoundary"
    )

    print(response)
    
    return "attached"
