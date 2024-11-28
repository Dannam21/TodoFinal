import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    body = event['body']
    tenant_id = body['tenant_id']
    producto_id = body['producto_id']

    response = table.delete_item(
        Key={'tenantID': tenant_id, 'productoID': producto_id}
    )

    return {
        'statusCode': 200,
        'body': 'Producto eliminado'
    }
