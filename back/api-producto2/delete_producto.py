import boto3
import os
import json

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

        # Eliminar el producto
        response = table.delete_item(
            Key={
                'tenant_id': tenant_id,  # Usar el nombre correcto de la clave
                'producto_id': producto_id  # Usar el nombre correcto de la clave
            }
        )

        # Verificar si se eliminó el producto
        if 'Attributes' not in response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Producto no encontrado'})
            }

        # Respuesta de éxito
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Producto eliminado'})
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error eliminando el producto: {str(e)}'})
        }
