import boto3
import os
import logging

# Configura el logging
logging.basicConfig(level=logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        tenant_id = event['queryStringParameters']['tenant_id']
        limit = int(event['queryStringParameters'].get('limit', 10))
        
        logging.info(f"tenant_id: {tenant_id}, limit: {limit}")

        # Realiza la consulta en DynamoDB
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('tenant_id').eq(tenant_id),
            Limit=limit
        )

        items = response.get('Items', [])
        logging.info(f"Items found: {items}")

        return {
            'statusCode': 200,
            'body': {
                'categorias': items
            }
        }
    
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': {
                'message': f"Internal Server Error: {str(e)}"
            }
        }
