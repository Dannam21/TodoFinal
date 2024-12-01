import boto3
import uuid
import os
import json
import logging
from boto3.dynamodb.conditions import Key

# Configuración de logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Inicialización de recursos DynamoDB
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['PRODUCTO_TABLE']  # Asegúrate de que esta variable esté correctamente configurada
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        logger.info("Received event: %s", json.dumps(event))

        # Obtener el cuerpo de la solicitud
        body = json.loads(event['body'])
        
        # Obtener los parámetros
        tenant_id = body.get('tenant_id')
        categoria_nombre = body.get('categoria_nombre')
        nombre = body.get('nombre')
        stock = body.get('stock')
        precio = body.get('precio')

        # Validación de parámetros obligatorios
        if not tenant_id or not categoria_nombre or not nombre or not stock or not precio:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Missing required data (tenant_id, categoria_nombre, nombre, stock, precio)'
                })
            }

        # Crear un nuevo ID de producto único
        producto_id = str(uuid.uuid4())

        # Crear la clave de partición utilizando tenant_id y categoria_nombre
        partition_key = f"{tenant_id}#{categoria_nombre}"

        # Verificar si ya existe un producto con ese nombre en esa categoría y con ese stock
        response = table.query(
            KeyConditionExpression=Key('tenant_id#categoria_nombre').eq(partition_key) & Key('stock').eq(stock)
        )

        if response['Items']:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Product already exists for this name in this category with this stock'
                })
            }

        # Crear el nuevo producto
        producto = {
            'tenant_id#categoria_nombre': partition_key,  # Clave de partición
            'producto_id': producto_id,  # Clave de ordenamiento
            'tenant_id': tenant_id,
            'categoria_nombre': categoria_nombre,
            'nombre': nombre,
            'stock': stock,
            'precio': precio
        }

        # Insertar el producto en la base de datos
        table.put_item(Item=producto)

        # Responder con un mensaje de éxito
        return {
            'statusCode': 201,
            'body': json.dumps({
                'message': 'Producto creado',
                'producto': producto
            })
        }

    except Exception as e:
        logger.error("Error creando el producto: %s", str(e))
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Error creando el producto: {str(e)}'
            })
        }
