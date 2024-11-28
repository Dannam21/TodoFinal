import boto3
import json
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
TOKENS_TABLE = 't_tokens_acceso'
tokens_table = dynamodb.Table(TOKENS_TABLE)

def lambda_handler(event, context):
    try:
        # Log the received event
        token = event['queryStringParameters']['token']

        # Fetch the token record from DynamoDB
        response = tokens_table.get_item(Key={'token': token})
        item = response.get('Item')

        if not item:
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Token no válido'})
            }

        # Check if the token has expired
        expires = datetime.strptime(item['expires'], '%Y-%m-%d %H:%M:%S')
        if datetime.utcnow() > expires:
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Token expirado'})
            }

        # Token is valid
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Token válido'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }