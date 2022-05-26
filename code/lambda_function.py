import json

def lambda_handler(event, context): # pylint: disable=unused-argument
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
