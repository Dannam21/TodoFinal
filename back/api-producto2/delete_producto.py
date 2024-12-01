import boto3
import os
import json
from decimal import Decimal


# Inicializar recursos DynamoDB
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Decodificar el cuerpo de la solicitud
        body = json.loads(event['body'])

        # Extraer parámetros
        tenant_id = body.get('tenant_id')
        producto_id = body.get('producto_id')

        # Validar parámetros
        if not tenant_id or not producto_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'tenant_id y producto_id son requeridos'})
            }

        # Intentar eliminar el producto
        response = table.delete_item(
            Key={
                'tenant_id': tenant_id,
                'producto_id': producto_id
            },
            ReturnValues="ALL_OLD"  # Solicitar los datos del producto eliminado
        )

        # Verificar si el producto existía
        if 'Attributes' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Producto no encontrado'})
            }

        # Respuesta de éxito
        return {
            'statusCode': 204
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error eliminando el producto: {str(e)}'})
        }
