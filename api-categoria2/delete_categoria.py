import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    body = event['body']
    tenant_id = body['tenant_id']
    categoria_id = body['categoria_id']

    response = table.delete_item(
        Key={'tenantID': tenant_id, 'categoriaID': categoria_id}
    )

    return {
        'statusCode': 200,
        'body': 'Categoría eliminada'
    }
