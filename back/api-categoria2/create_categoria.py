import boto3
import uuid
import datetime
import os
import json  # Importar json para deserializar el cuerpo si es necesario

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    # Obtener el cuerpo de la solicitud
    body = event['body']
    
    # Verificar si 'body' es una cadena JSON, y si es así, convertirla a diccionario
    if isinstance(body, str):
        body = json.loads(body)  # Deserializar el string JSON en un diccionario
    
    # Extraer los datos del cuerpo deserializado
    tenant_id = body['tenant_id']
    categoria_id = str(uuid.uuid4())
    nombre = body['nombre']
    fecha_creacion = datetime.datetime.utcnow().isoformat()
    data = body.get('data')

    # Crear el objeto de categoría que se va a guardar en DynamoDB
    categoria = {
        'tenant_id': tenant_id,
        'categoria_id': categoria_id,
        'nombre': nombre,
        'data': data
    }

    # Guardar el objeto de categoría en DynamoDB
    response = table.put_item(Item=categoria)

    # Retornar una respuesta exitosa
    return {
        'statusCode': 201,
        'body': json.dumps({  # Asegurarse de que el cuerpo de la respuesta esté serializado en JSON
            'message': 'Categoría creada',
            'categoria_id': categoria_id
        })
    }
