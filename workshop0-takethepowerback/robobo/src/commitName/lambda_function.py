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
    response = dynamoclient.update_item(
        TableName = event['nameTable'],
        Key = {
            'id': {
                'S': event['instanceName']
            }
        },
        ExpressionAttributeNames = {
            '#STATE': 'state',
            '#TIMESTAMP': 'stateTimeStamp'
        },
        ExpressionAttributeValues = {
            ':st': {
                'S': 'PROVISIONED'
            },
            ':ts': {
                'S': time.strftime("%Y %m %d - %H:%M%z")
            }
        },
        UpdateExpression = 'SET #STATE = :st, #TIMESTAMP = :ts'
    )
    return response