import boto3
import os
import json

dynamodb = boto3.resource('dynamodb')
USERS_TABLE = os.environ['USERS_TABLE']
table = dynamodb.Table(USERS_TABLE)

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        tenant_id = body.get('tenant_id')
        user_id = body.get('user_id')
        email = body.get('email')
        
        token = event['headers'].get('Authorization')

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


        # Si tenemos tenant_id y email, usamos otro índice en DynamoDB
        elif tenant_id and email:
            response = table.query(
                IndexName='BusquedaPorEmail',  # El nombre del índice LSI
                KeyConditionExpression=Key('tenant_id').eq(tenant_id) & Key('email').eq(email)
            )
        
            if len(response.get('Items', [])) > 0:
                user_item = response['Items'][0]
                payload = {
                    "token": token,
                    "tenant_id": user_item['tenant_id'],
                    "user_id": user_item['user_id']
                }

                # Invocar la función de validación del token
                invoke_response = lambda_client.invoke(
                    FunctionName="ValidarTokenAcceso",
                    InvocationType='RequestResponse',
                    Payload=json.dumps(payload)
                )

                response1 = json.loads(invoke_response['Payload'].read().decode())
                print(response1)
                if response1['statusCode'] == 403:
                    return {
                        'statusCode': 403,
                        'body': json.dumps({'error': 'Forbidden - Acceso No Autorizado'})
                    }
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

        response = table.delete_item(Key={'tenant_id': tenant_id, 'user_id': user_id})

        return {
            'statusCode': 204,
            'body': 'Usuario eliminado'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }