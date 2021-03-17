import boto3
from botocore.config import Config
import os
import time

boto_config = Config(
        region_name = os.environ['AWS_REGION'],
        retries = {
            'mode': 'standard'
        }
)

dynamoclient = boto3.client('dynamodb', config = boto_config)

def lambda_handler(event, context):
    response = dynamoclient.put_item(
        TableName = event['nameTable'],
        Item = {
            'id': {
                'S': event['instanceName']
            },
            'state': {
                'S': 'RESERVED'
            },
            'stateTimeStamp': {
                'S': time.strftime("%Y %m %d - %H:%M%z")
            }
        }
    )
    return response