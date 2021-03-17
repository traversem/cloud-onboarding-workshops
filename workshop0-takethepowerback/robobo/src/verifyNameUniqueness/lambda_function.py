import boto3
from botocore.config import Config
import os
import json

boto_config = Config(
        region_name = os.environ['AWS_REGION'],
        retries = {
            'mode': 'standard'
        }
)

dynamoclient = boto3.client('dynamodb', config = boto_config)

def lambda_handler(event, context):
    response = dynamoclient.get_item(
        TableName = event['nameTable'],
        Key = {
            'id': {
                'S': event['instanceName']
            }
        },
        ConsistentRead = True
    )
    if not 'Item' in response:
        nameInUse = False
    else:
        nameInUse = True
    return nameInUse