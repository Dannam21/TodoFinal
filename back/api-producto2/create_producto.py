import boto3
import uuid
import os
import json

from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        logger.info("Received event: %s", json.dumps(event))

        body = json.loads(event['body'])
        data = body.get('data')

        tenant_id = body.get('tenant_id')
        producto_id = str(uuid.uuid4())
        categoria_nombre = body['categoria_nombre']
        nombre = body['nombre']
        stock = body['stock']
        precio = body['precio']

        if not tenant_id or not producto_id or not categoria_nombre or not nombre or not stock or not precio:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Missing data values'})
            }

        response = table.query(
            IndexName='BusquedaPorNombre',  # El nombre del índice LSI
            KeyConditionExpression=Key('tenant_id').eq(tenant_id) & Key('nombre').eq(nombre)
        )

        if response['Items']:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Product already exists for this name'})
            }

        producto = {
            'tenantID': tenant_id,
            'productoID': producto_id,
            'categoriaNombre': categoria_nombre,
            'nombre': nombre,
            'stock': stock,
            'precio': precio
        }

        response = table.put_item(Item=producto)

        return {
            'statusCode': 201,
            'body': {
                'message': 'Producto creado',
                'tenantID': tenant_id,
                'productoID': producto_id,
                'categoriaNombre': categoria_nombre,
                'nombre': nombre,
                'stock': stock,
                'precio': precio
            }
        }
    except Exception as e:
        logger.error("Error creating product: %s", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
