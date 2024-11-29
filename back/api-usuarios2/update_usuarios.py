import boto3
import os
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
USERS_TABLE = os.environ['USERS_TABLE']
table = dynamodb.Table(USERS_TABLE)

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])

        tenant_id = body['tenant_id']#obligatorio
        user_id = body['user_id']#obligatorio

        email = body.get('email')
        data = body.get('data')

        update_expression = "set "
        expression_attribute_values = {}

        token = event['headers']['Authorization']
        lambda_client = boto3.client('lambda')    

        payload_string = json.dumps({
            "token": token,
            "tenant_id": tenant_id,
            "user_id": user_id
        })


        invoke_response = lambda_client.invoke(
            FunctionName="validarTokenAcceso",
            InvocationType='RequestResponse',
            Payload=payload_string
        )
        
        response1 = json.loads(invoke_response['Payload'].read())
        if response1['statusCode'] == 403:
            return {
                'statusCode' : 403,
                'status' : 'Forbidden - Acceso No Autorizado'
            }

        if data:
            update_expression += "data = :data, "
            expression_attribute_values[':data'] = data

        if email:
            ##
            response = table.query(
            IndexName='BusquedaPorEmail',  # El nombre del índice LSI
            KeyConditionExpression=Key('tenant_id').eq(tenant_id) & Key('email').eq(email)
            )
            if response['Items']:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Email already exists for this tenant'})
                }

            ##
            update_expression += "email = :email, "
            expression_attribute_values[':email'] = email


        update_expression = update_expression.rstrip(', ')

        response = table.update_item(
            Key={'tenant_id': tenant_id, 'user_id': user_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_attribute_values,
            ReturnValues="UPDATED_NEW"
        )

        return {
            'statusCode': 200,
            'body': json.dumps(response['Attributes'])
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }