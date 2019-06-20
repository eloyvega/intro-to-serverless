import os
import json
import uuid
import time
import calendar

import boto3


dynamo_table = boto3.resource('dynamodb').Table(os.environ['DYNAMO_TABLE'])

def main(event, context):
    print(json.dumps(event))
    record = json.loads(event['body'])
    record['id'] = str(uuid.uuid4())
    record['timestamp'] = str(calendar.timegm(time.gmtime()))
    
    dynamo_table.put_item(Item=record)
    api_response = {
        'statusCode': 200,
        'body': json.dumps({'task': record, 'status': 200}),
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        }
    }

    return api_response