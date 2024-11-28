import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    categoria_id = event['queryStringParameters']['categoriaID']
    tenant_id = event['queryStringParameters']['tenantID']

    response = table.get_item(
        Key={'tenantID': tenant_id, 'categoriaID': categoria_id}
    )

    item = response.get('Item')

    if not item:
        return {
            'statusCode': 404,
            'body': 'Categoría no encontrada'
        }

    return {
        'statusCode': 200,
        'body': item
    }
