import boto3
from botocore.config import Config
import os

boto_config = Config(
        region_name = os.environ['AWS_REGION'],
        retries = {
            'mode': 'standard'
        }
)

ec2client = boto3.client('ec2', config = boto_config)

def handle_request(intent):
    
    return

def run_instances(event):
    print(event)
    response = ec2client.run_instances(
        ImageId = event['amiId'],
        InstanceType = event['instanceType'],
        MaxCount = 1,
        MinCount = 1,
        SecurityGroupIds = event['securitygroupIds'],
        SubnetId = event['subnetId'],
        TagSpecifications = [
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': event['instanceName']
                    },
                    {
                        'Key': 'AppName',
                        'Value': 'sample-app'
                    },
                    {
                        'Key': 'deploymentType',
                        'Value': 'with luv by alexa'
                    }
                ]
            }
        ]
    )
    response = {
        'instanceId': response['Instances'][0]['InstanceId'],
        'instanceName': event['instanceName']
    }
    return response

def handle_error():
    response = 'an error occured handling the request'
    return response

def lambda_handler(event, context):
    response = run_instances(event)
#    try:
#        response = run_instance()
#    except:
#        response = handle_error()
    return response