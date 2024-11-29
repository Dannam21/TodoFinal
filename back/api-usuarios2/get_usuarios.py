import boto3
import os
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
USERS_TABLE = os.environ['USERS_TABLE']
table = dynamodb.Table(USERS_TABLE)

def lambda_handler(event, context):
    # Obtener los parámetros de la consulta directamente
    params = event.get('queryStringParameters', {})
    tenant_id = params.get('tenant_id')
    user_id = params.get('user_id')
    email = params.get('email')
    print(params)

    # Obtener el token de autorización
    token = event['headers'].get('Authorization')
    
    if not token:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Authorization token is missing'})
        }

    # Crear el cliente de Lambda para invocar la función de validación del token
    lambda_client = boto3.client('lambda')

    # Verificar si tenemos tenant_id y user_id
    if tenant_id and user_id:
        payload = {
            "token": token,
            "tenant_id": tenant_id,
            "user_id": user_id
        }

        # Invocar la función de validación del token
        invoke_response = lambda_client.invoke(
            FunctionName="ValidarTokenAcceso",  # Asegúrate de que este sea el nombre correcto
            InvocationType='RequestResponse',
            Payload=json.dumps(payload)
        )

        # Leer la respuesta de la función de validación
        response1 = json.loads(invoke_response['Payload'].read().decode())
        if response1['statusCode'] == 403:
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Forbidden - Acceso No Autorizado'})
            }

        # Consultar el usuario en DynamoDB
        response = table.get_item(Key={'tenant_id': tenant_id, 'user_id': user_id})

    # Si tenemos tenant_id y email, usamos otro índice en DynamoDB
    elif tenant_id and email:
        response = table.query(
            IndexName='BusquedaPorEmail',  # El nombre del índice LSI
            KeyConditionExpression=Key('tenant_id').eq(tenant_id) & Key('email').eq(email)
        )

        if response.get('Items'):
            user_item = response['Items'][0]
            payload = {
                "token": token,
                "tenant_id": user_item['tenant_id'],
                "user_id": user_item['user_id']
            }

            # Invocar la función de validación del token
            invoke_response = lambda_client.invoke(
                FunctionName="validarTokenAcceso",
                InvocationType='RequestResponse',
                Payload=json.dumps(payload)
            )

            response1 = json.loads(invoke_response['Payload'].read().decode())
            if response1['statusCode'] == 403:
                return {
                    'statusCode': 403,
                    'body': json.dumps({'error': 'Forbidden - Acceso No Autorizado'})
                }

            # Si el token es válido, devolvemos los datos del usuario
            item = user_item
        else:
            return {
                'statusCode': 404,
                'body': json.dumps({'error': 'Usuario no encontrado'})
            }
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Debe proporcionar tenant_id y user_id o tenant_id y email'})
        }

    # Obtener el ítem de la respuesta de DynamoDB
    item = response.get('Item') if 'Item' in response else None

    if not item:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Usuario no encontrado'})
        }

    # Eliminar el campo 'password' si existe antes de devolver los datos
    item.pop('password', None)

    return {
        'statusCode': 200,
        'body': json.dumps(item)
    }
