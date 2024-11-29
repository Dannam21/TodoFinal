import boto3
import os
import json
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
USERS_TABLE = os.environ['USERS_TABLE']
table = dynamodb.Table(USERS_TABLE)

def lambda_handler(event, context):
    tenant_id = event.get('queryStringParameters', {}).get('tenant_id')
    user_id = event.get('queryStringParameters', {}).get('user_id')
    email = event.get('queryStringParameters', {}).get('email')

    token = event['headers']['Authorization']
    lambda_client = boto3.client('lambda')    
    # payload_string = '{ "token": "' + token +','+ '"tenant_id": "' + tenant_id + ','+ '"user_id": "' + user_id+'" }'
    # invoke_response = lambda_client.invoke(FunctionName="ValidarTokenAcceso",
    #                                        InvocationType='RequestResponse',
    #                                        Payload = payload_string)
    # response1 = json.loads(invoke_response['Payload'].read())
    # print(response1)

    
    if tenant_id and user_id:
        ##
        payload_string = json.dumps({
            "token": token,
            "tenant_id": tenant_id,
            "user_id": user_id
        })

        invoke_response = lambda_client.invoke(FunctionName="ValidarTokenAcceso",
                                           InvocationType='RequestResponse',
                                           Payload = payload_string)
        response1 = json.loads(invoke_response['Payload'].read())
        if response1['statusCode'] == 403:
            return {
                'statusCode' : 403,
                'status' : 'Forbidden - Acceso No Autorizado'
            }
        ##
        response = table.get_item(Key={'tenant_id': tenant_id, 'user_id': user_id})
    elif tenant_id and email:
        response = table.query(
            IndexName='BusquedaPorEmail',  # El nombre del índice LSI
            KeyConditionExpression=Key('tenant_id').eq(tenant_id) & Key('email').eq(email)
        )
        payload_string = '{ "token": "' + token +','+ '"tenant_id": "' + response['tenant_id'] + ','+ '"user_id": "' + response['user_id']+'" }'
        invoke_response = lambda_client.invoke(FunctionName="validarTokenAcceso",
                                            InvocationType='RequestResponse',
                                            Payload = payload_string)
        response1 = json.loads(invoke_response['Payload'].read())
        if response1['statusCode'] == 403:
            return {
                'statusCode' : 403,
                'status' : 'Forbidden - Acceso No Autorizado'
            }
    else:
        return {'statusCode': 400, 'body': 'Debe proporcionar tenant_id y user_id o tenant_id y email'}

    item = response.get('Item') if 'Item' in response else response.get('Items', [None])[0]

    if not item:
        return {'statusCode': 404, 'body': 'Usuario no encontrado'}

    item.pop('password', None)
    return {
        'statusCode': 200,
        'body': item
    }