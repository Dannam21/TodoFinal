import boto3
import uuid
import datetime
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    body = event['body']
    tenant_id = body['tenant_id']
    nombre = body['nombre']
    precio = body['precio']
    categoria_id = body['categoria_id']
    producto_id = str(uuid.uuid4())
    fecha_creacion = datetime.datetime.utcnow().isoformat()

    producto = {
        'tenantID': tenant_id,
        'productoID': producto_id,
        'nombre': nombre,
        'precio': precio,
        'categoriaID': categoria_id,
        'fechaCreacion': fecha_creacion
    }

    response = table.put_item(Item=producto)

    return {
        'statusCode': 201,
        'body': {
            'message': 'Producto creado',
            'productoID': producto_id,
            'fechaCreacion': fecha_creacion
        }
    }
