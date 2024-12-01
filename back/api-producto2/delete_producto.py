import boto3
import os
import json
from datetime import datetime

# Inicializar recursos DynamoDB
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

TOKENS_TABLE = os.environ['TOKENS_TABLE']
tokens_table = dynamodb.Table(TOKENS_TABLE)

def lambda_handler(event, context):
    try:
        # Decodificar el cuerpo de la solicitud
        body = json.loads(event['body'])

        # Extraer parámetros
        token = body.get('token')
        tenant_id = body.get('tenant_id')
        producto_id = body.get('producto_id')

        # Validar parámetros
        if not token or not tenant_id or not producto_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'token, tenant_id y producto_id son requeridos'})
            }

        # Validar el token en la tabla de tokens
        token_response = tokens_table.get_item(Key={'token': token})
        token_data = token_response.get('Item')

        if not token_data:
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Token no válido'})
            }

        # Verificar si el token ha expirado
        expires = datetime.strptime(token_data['expires'], '%Y-%m-%d %H:%M:%S')
        if datetime.utcnow() > expires:
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Token expirado'})
            }

        # Validar si el rol es "admin"
        if token_data.get('role') != 'admin':
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Solo los administradores pueden eliminar productos'})
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
