import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    body = event['body']
    tenant_id = body['tenant_id']
    categoria_id = body['categoria_id']
    nuevo_nombre = body['nuevo_nombre']

    response = table.update_item(
        Key={'tenantID': tenant_id, 'categoriaID': categoria_id},
        UpdateExpression="SET nombre = :nombre",
        ExpressionAttributeValues={':nombre': nuevo_nombre},
        ReturnValues="ALL_NEW"
    )

    return {
        'statusCode': 200,
        'body': response['Attributes']
    }
