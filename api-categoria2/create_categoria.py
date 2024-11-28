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
    categoria_id = str(uuid.uuid4())
    fecha_creacion = datetime.datetime.utcnow().isoformat()

    categoria = {
        'tenantID': tenant_id,
        'categoriaID': categoria_id,
        'nombre': nombre,
        'fechaCreacion': fecha_creacion
    }

    response = table.put_item(Item=categoria)

    return {
        'statusCode': 201,
        'body': {
            'message': 'Categoría creada',
            'categoriaID': categoria_id,
            'fechaCreacion': fecha_creacion
        }
    }
