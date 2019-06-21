import os
import json

import boto3


dynamo_table = boto3.resource('dynamodb').Table(os.environ['DYNAMO_TABLE'])

def main(event, context):
    print(json.dumps(event))
    items = []
    response = dynamo_table.scan()
    items += response['Items']
    while 'LastEvaluatedKey' in response:
        response = dynamo_table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        items += response['Items']
    sorted_response = sorted(items, key=lambda k: k['timestamp'], reverse=True)
    api_response = {
        'statusCode': 200,
        'body': json.dumps(sorted_response),
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
    }
    return api_response