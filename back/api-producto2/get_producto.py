import boto3
import os
import json

# Inicialización de DynamoDB
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Obtener los parámetros de consulta
        producto_id = event['queryStringParameters']['producto_id']
        tenant_id = event['queryStringParameters']['tenant_id']
        categoria_nombre = event['queryStringParameters']['categoria_nombre']

        # Crear la clave de partición combinando tenant_id y categoria_nombre
        partition_key = f"{tenant_id}#{categoria_nombre}"

        # Realizar la consulta usando la clave de partición y la clave de ordenamiento (producto_id)
        response = table.get_item(
            Key={
                'tenant_id#categoria_nombre': partition_key,  # Clave de partición correcta
                'producto_id': producto_id  # Clave de ordenamiento correcta
            }
        )

        # Obtener el artículo de la respuesta
        item = response.get('Item')

        # Si no se encuentra el producto
        if not item:
            return {
                'statusCode': 404,
                'body': json.dumps({
                    'error': 'Producto no encontrado'
                })
            }

        # Si se encuentra el producto
        return {
            'statusCode': 200,
            'body': json.dumps(item)
        }

    except Exception as e:
        # En caso de error
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Error al obtener el producto: {str(e)}'
            })
        }
