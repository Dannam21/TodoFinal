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
        producto_id = event['queryStringParameters'].get('producto_id')

        # Validación de parámetros obligatorios
        if not tenant_id or not categoria_nombre or not producto_id:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Missing required parameters (tenant_id, categoria_nombre, producto_id)'
                })
            }

        # Crear la clave de partición y clave de ordenamiento
        partition_key = f"{tenant_id}#{categoria_nombre}"

        # Realizar la consulta para obtener el producto por producto_id
        response = table.get_item(
            Key={
                'tenant_id#categoria_nombre': partition_key,
                'producto_id': producto_id
            }
        )

        # Verificar si el producto existe
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'message': 'Producto no encontrado para el producto_id y la combinación de tenant_id y categoria_nombre'
                })
            }

        # Devolver el producto encontrado
        return {
            'statusCode': 200,
            'body': json.dumps({
                'producto': response['Item']
            })
        }

    except Exception as e:
        logger.error("Error obteniendo el producto: %s", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Error obteniendo el producto: {str(e)}'
            })
        }
