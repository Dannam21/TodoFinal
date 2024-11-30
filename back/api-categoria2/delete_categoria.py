import boto3
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
    categoria_id = body['categoria_id']

    # Eliminar el item de DynamoDB
    response = table.delete_item(
        Key={'tenant_id': tenant_id, 'categoria_id': categoria_id}
    )

    # Retornar una respuesta exitosa
    return {
        'statusCode': 200,
        'body': json.dumps('Categoría eliminada')  # Asegurarse de que la respuesta sea un JSON
    }
