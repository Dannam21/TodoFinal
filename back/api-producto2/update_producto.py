import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    body = event['body']
    tenant_id = body['tenant_id']
    producto_id = body['producto_id']
    updates = body['updates']

    update_expression = "SET "
    expression_values = {}

    for key, value in updates.items():
        update_expression += f" {key} = :{key},"
        expression_values[f":{key}"] = value

    update_expression = update_expression.rstrip(',')

    response = table.update_item(
        Key={'tenantID': tenant_id, 'productoID': producto_id},
        UpdateExpression=update_expression,
        ExpressionAttributeValues=expression_values,
        ReturnValues="ALL_NEW"
    )

    return {
        'statusCode': 200,
        'body': response['Attributes']
    }
