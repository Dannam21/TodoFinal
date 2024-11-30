import boto3
import os
import logging

# Configuración de logging para ver los registros en CloudWatch
logging.basicConfig(level=logging.INFO)

# Inicialización de DynamoDB
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'DefaultTable')  # Nombre de la tabla DynamoDB
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Registra todo el contenido del evento
        logging.info(f"Event received: {event}")
        
        # Accede a los parámetros queryStringParameters
        tenant_id = event['queryStringParameters'].get('tenant_id', None)
        limit = int(event['queryStringParameters'].get('limit', 10))
        
        # Verifica si el tenant_id está presente
        if not tenant_id:
            logging.error("tenant_id is missing")
            return {
                'statusCode': 400,
                'body': {'message': 'tenant_id is required'}
            }

        logging.info(f"tenant_id: {tenant_id}, limit: {limit}")
        
        # Realiza la consulta en DynamoDB
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('tenant_id').eq(tenant_id),
            Limit=limit
        )
        
        # Registra la respuesta de DynamoDB
        items = response.get('Items', [])
        logging.info(f"Items found: {items}")

        return {
            'statusCode': 200,
            'body': {
                'categorias': items
            }
        }
    
    except Exception as e:
        # Captura cualquier error inesperado
        logging.error(f"Unexpected error: {str(e)}")
        return {
            'statusCode': 500,
            'body': {
                'message': f"Internal Server Error: {str(e)}"
            }
        }
