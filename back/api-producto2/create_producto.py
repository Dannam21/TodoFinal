import boto3
import uuid
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

        # Obtener el cuerpo de la solicitud
        body = json.loads(event['body'])
        
        # Obtener los parámetros
        tenant_id = body.get('tenant_id')
        categoria_nombre = body.get('categoria_nombre')
        nombre = body.get('nombre')
        stock = body.get('stock')  # Se espera que 'stock' sea un número entero
        precio = body.get('precio')

        # Validación de parámetros obligatorios
        if not tenant_id or not categoria_nombre or not nombre or stock is None or not precio:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Missing required data (tenant_id, categoria_nombre, nombre, stock, precio)'
                })
            }

        # Asegúrate de convertir el stock a int si es necesario
        try:
            stock = int(stock)  # Convertir a entero
        except ValueError:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'El stock debe ser un número entero válido'
                })
            }

        # Crear un nuevo ID de producto único
        producto_id = str(uuid.uuid4())

        # Crear la clave de partición utilizando tenant_id y categoria_nombre
        partition_key = f"{tenant_id}#{categoria_nombre}"

        # Crear el nuevo producto
        producto = {
            'tenant_id#categoria_nombre': partition_key,  # Clave de partición
            'producto_id': producto_id,  # Clave de ordenamiento
            'tenant_id': tenant_id,
            'categoria_nombre': categoria_nombre,
            'nombre': nombre,
            'stock': stock,  # Guardar como int
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
