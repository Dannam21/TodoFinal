import boto3
import os
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
USERS_TABLE = os.environ['USERS_TABLE']
table = dynamodb.Table(USERS_TABLE)

def lambda_handler(event, context):
    try:
        # Parsear el cuerpo de la solicitud
        body = json.loads(event['body'])

        tenant_id = body['tenant_id']  # obligatorio
        user_id = body['user_id']  # obligatorio

        email = body.get('email')
        data = body.get('data')

        # Inicializar la expresión de actualización
        update_expression = "set "
        expression_attribute_values = {}

        # Obtener el token del encabezado Authorization
        token = event['headers'].get('Authorization')
        if not token:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Authorization header is missing'})
            }

        # Aquí construimos el diccionario con los parámetros necesarios
        payload_dict = {
            "token": token,  # El valor del token que debería llegar como 'Bearer <token>'
            "tenant_id": tenant_id,
            "user_id": user_id
        }

        # Convertir el diccionario a una cadena JSON válida
        payload_string = json.dumps(payload_dict)

        # Invocar la función Lambda para validar el token
        lambda_client = boto3.client('lambda')
        invoke_response = lambda_client.invoke(
            FunctionName="validar_token_acceso",
            InvocationType='RequestResponse',
            Payload=payload_string
        )

        # Procesar la respuesta de la función Lambda
        response1 = json.loads(invoke_response['Payload'].read().decode())
        if response1.get('statusCode') == 403:
            return {
                'statusCode': 403,
                'body': json.dumps({'status': 'Forbidden - Acceso No Autorizado'})
            }

        # Si hay datos para actualizar, agregarlos a la expresión de actualización
        if data:
            update_expression += "data = :data, "
            expression_attribute_values[':data'] = data

        # Si se proporciona un email, verificar si ya existe en el sistema
        if email:
            response = table.query(
                IndexName='BusquedaPorEmail',  # El nombre del índice LSI
                KeyConditionExpression=Key('tenant_id').eq(tenant_id) & Key('email').eq(email)
            )
            if response['Items']:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Email already exists for this tenant'})
                }

            update_expression += "email = :email, "
            expression_attribute_values[':email'] = email

        # Eliminar la última coma de la expresión de actualización
        update_expression = update_expression.rstrip(', ')

        # Actualizar el item en la tabla DynamoDB
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
