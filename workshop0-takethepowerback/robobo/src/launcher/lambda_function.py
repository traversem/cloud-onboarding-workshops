import boto3
from botocore.config import Config
import os
import uuid
import json

boto_config = Config(
        region_name = os.environ['AWS_REGION'],
        retries = {
            'mode': 'standard'
        }
)

ssmclient = boto3.client('ssm', config = boto_config)
stepclient = boto3.client('stepfunctions', config = boto_config)

def handle_request(intent):
    
    return

def build_response(status, payload):
    if status == 'success':
        count = payload['count']
        os = payload['os']
        if count < 5:
            output = f'le déploiement de {count} instances {os} est en cours'
        else:
            output = f'tu es pas fou, plus de cinq instances à la fois? je rigole, pas de problème je suis pas le b.o. workflow. Lancement de {count} instances en cours'
    elif status == 'failure':
        output = f'échec du déploiement demandé'
    
    response = {
        'version': '1.0',
        'response': {
            'outputSpeech': {
                'text': str(output),
                'type': 'PlainText'
            },
            'shouldEndSession': True
        }
    }
    return response

class get_unique_parameter():
    def fetch(self, parameter):
        response = ssmclient.get_parameter(
            Name = parameter
        )['Parameter']['Value']
        return response

def build_payload(**kwargs):
    parameter = get_unique_parameter()
    count = int(kwargs.get('count'))
    instance_type = parameter.fetch(os.environ['instanceTypeParameter'])
    vpc_id = parameter.fetch(os.environ['vpcIdParameter'])
    subnet_id = parameter.fetch(os.environ['subnetIdParameter'])
    securitygroup_ids = parameter.fetch(os.environ['securityGroupIdsParameter']).split()
    name_table = parameter.fetch(os.environ['nameTableParameter'])
    if kwargs.get('os') == 'linux':
        ami_id = parameter.fetch(os.environ['linuxAmiParameter'])
        print('this is linux')
    elif kwargs.get('os') == 'windows':
        ami_id = parameter.fetch(os.environ['windowsAmiParameter'])
        print('this is windows')
    response = {
        'os': kwargs.get('os'),
        'instanceType': instance_type,
        'amiId': ami_id,
        'count': count,
        'vpcId': vpc_id,
        'subnetId': subnet_id,
        'securitygroupIds': securitygroup_ids,
        'nameTable': name_table
    }
    print(response)
    return response

def launch_pipeline(payload):
    parameter = get_unique_parameter()
    response = stepclient.start_execution(
        stateMachineArn = parameter.fetch(os.environ['deploymentPipelineParameter']),
        name = str(uuid.uuid4()),
        input = json.dumps(payload)
    )
    return response

def handle_error():
    response = 'an error occured handling the request'
    return response

def lambda_handler(event, context):
    print(event)
    try:
        assert 'intent' in event['request']
        print(event['request'])
        assert 'slots' in event['request']['intent']
        print(event['request']['intent']['slots'])
        assert 'os' in event['request']['intent']['slots']
        os = event['request']['intent']['slots']['os']['value']
        assert 'count' in event['request']['intent']['slots']
        count = event['request']['intent']['slots']['count']['value']
        payload = build_payload(os = os, count = count)
        execution = launch_pipeline(payload)
        response = build_response('success', payload)
    except:
        payload = {}
        response = build_response('failure', payload)
    print(response)
    return response