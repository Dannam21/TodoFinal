import boto3
import os
import logging 
import json

def lambda_handler(event, context):
    try:
        table_name = os.environ.get('TABLE_NAME', 'DefaultTable') 
        print(table_name)
        logging.info(f"Event recibido: {event}")
        
        # Accede a los parámetros queryStringParameters
        tenant_id = event['queryStringParameters'].get('tenant_id', None)
        limit = event['queryStringParameters'].get('limit', 10)
        
        if tenant_id is None:
            logging.error("tenant_id es obligatorio")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'tenant_id es obligatorio'})
            }
        
        try:
            limit = int(limit)
        except ValueError:
            logging.error("Limit no es un número válido")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'limit debe ser un número entero'})
            }

        logging.info(f"Parámetros recibidos - tenant_id: {tenant_id}, limit: {limit}")
        
        response = table_name.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('tenant_id').eq(tenant_id),
            Limit=limit
        )

        items = response.get('Items', [])

        logging.info(f"Items encontrados: {items}")

        return {
            'statusCode': 200,
            'body': json.dumps({'categorias': items})  # Convertimos a JSON
        }
    
    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f"Error interno del servidor: {str(e)}"})
        }
