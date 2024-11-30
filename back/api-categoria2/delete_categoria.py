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

    # Agregar depuración para ver los valores recibidos
    print(f"Received categoria_id: {categoria_id}, tenant_id: {tenant_id}")

    try:
        # Eliminar el item usando categoria_id y tenant_id como claves
        response = table.delete_item(
            Key={
                'categoria_id': categoria_id,
                'tenant_id': tenant_id
            }
        )

        # Comprobación de la respuesta para asegurar que el ítem se eliminó
        if 'Attributes' not in response:
            print(f"Item with categoria_id: {categoria_id} and tenant_id: {tenant_id} not found.")
            return {
                'statusCode': 404,
                'body': json.dumps('Categoría no encontrada')
            }

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
