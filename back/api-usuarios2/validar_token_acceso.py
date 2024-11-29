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
        tenant_id = event['queryStringParameters']['tenant_id']
        user_id = event['queryStringParameters']['user_id']
        # Fetch the token record from DynamoDB
        response = tokens_table.get_item(Key={'token': token})
        item = response.get('Item')

        if not item:
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Token no válido'})
            }
        if not((item["tenant_id"]==tenant_id and item["user_id"]==user_id) or item['role'] =="admin"):
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Token no válido para el tenant_id y user_id'})
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
            'body': json.dumps({'message': 'Token válido','tenant_id':item['tenant_id'],'user_id':item['user_id'],'role':item['role']})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }