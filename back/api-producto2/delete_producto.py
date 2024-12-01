import boto3
import logging
import os
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Parsear el cuerpo de la solicitud
        body = json.loads(event['body'])
        tenant_id = body.get('tenant_id')
        producto_id = body.get('producto_id')

        if not tenant_id or not producto_id:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Debe proporcionar tenant_id y producto_id'})
            }

        delete_response = table.delete_item(
            Key={'tenant_id': tenant_id, 'producto_id': producto_id}
        )

        if 'Attributes' not in delete_response:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Producto no encontrado'})
            }

        return {
            'statusCode': 204,
            'body': json.dumps({'message': 'Producto eliminado exitosamente'})
        }

    except Exception as e:
        logger.error("Error al eliminar el producto: %s", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f'Error interno: {str(e)}'})
        }
