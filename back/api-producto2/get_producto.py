import boto3
import os
import json
import logging

# Configuración de logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Inicialización de recursos DynamoDB
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        logger.info("Received event: %s", json.dumps(event))

        # Obtener los parámetros de la consulta
        tenant_id = event['queryStringParameters'].get('tenant_id')
        categoria_nombre = event['queryStringParameters'].get('categoria_nombre')

        # Validación de parámetros obligatorios
        if not tenant_id or not categoria_nombre:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Missing required parameters (tenant_id, categoria_nombre)'
                })
            }

        # Crear la clave de partición
        partition_key = f"{tenant_id}#{categoria_nombre}"

        # Realizar una consulta para obtener los productos
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('tenant_id#categoria_nombre').eq(partition_key)
        )

        # Verificar si hay productos
        if 'Items' not in response or not response['Items']:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'message': 'No products found for the given tenant_id and categoria_nombre'
                })
            }

        # Devolver los productos encontrados
        return {
            'statusCode': 200,
            'body': json.dumps({
                'productos': response['Items']
            })
        }

    except Exception as e:
        logger.error("Error obteniendo los productos: %s", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Error obteniendo los productos: {str(e)}'
            })
        }
