import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)


def lambda_handler(event, context):
    tenant_id = event['queryStringParameters']['tenantID']
    limit = int(event['queryStringParameters'].get('limit', 10))

    response = table.query(
        KeyConditionExpression=boto3.dynamodb.conditions.Key('tenantID').eq(tenant_id),
        Limit=limit
    )

    items = response.get('Items', [])

    return {
        'statusCode': 200,
        'body': {
            'categorias': items
        }
    }
