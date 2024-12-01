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

    token = event['headers'].get('Authorization')
    if not token:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Authorization token is missing'})
        }

        # Crear el cliente de Lambda para invocar la validación del token
    lambda_client = boto3.client('lambda')

        # Construir la carga útil para validar el token
    payload_string = json.dumps({
        "token": token,
        "tenant_id": tenant_id,
        "user_id": user_id
    })

        # Invocar la función de validación del token
    invoke_response = lambda_client.invoke(
        FunctionName="ValidarTokenAcceso",  # Asegúrate de que el nombre de la función sea correcto
        InvocationType='RequestResponse',
        Payload=payload_string
    )
    
        # Leer la respuesta de la validación del token
    response1 = json.loads(invoke_response['Payload'].read().decode())
    if response1['statusCode'] == 403:
        return {
            'statusCode': 403,
            'body': json.dumps({'error': 'Forbidden - Acceso No Autorizado'})
        }
    
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
