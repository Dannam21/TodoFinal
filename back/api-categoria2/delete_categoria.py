import boto3
import os
import json

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    body = event['body']

    # Deserializar si el body está en formato JSON
    if isinstance(body, str):
        body = json.loads(body)
    
    categoria_id = body['categoria_id']
    tenant_id = body['tenant_id']

    # Verificar si el ítem existe antes de eliminarlo
    response = table.get_item(
        Key={
            'categoria_id': categoria_id,
            'tenant_id': tenant_id
        }
    )

    if 'Item' not in response:
        print(f"Item with categoria_id: {categoria_id} and tenant_id: {tenant_id} not found.")
        return {
            'statusCode': 404,
            'body': json.dumps('Categoría no encontrada')
        }

    # Si el ítem existe, proceder con la eliminación
    try:
        delete_response = table.delete_item(
            Key={
                'categoria_id': categoria_id,
                'tenant_id': tenant_id
            }
        )

        return {
            'statusCode': 200,
            'body': json.dumps('Categoría eliminada con éxito')
        }

    except Exception as e:
        print(f"Error al eliminar la categoría: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error al eliminar la categoría: {str(e)}')
        }
