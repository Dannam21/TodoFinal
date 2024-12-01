import boto3
import json
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
TOKENS_TABLE = 't_tokens_acceso'
tokens_table = dynamodb.Table(TOKENS_TABLE)

def lambda_handler(event, context):
    try:
        # Log the received event
        params = event.get('queryStringParameters', {})
        token = params.get('token')
        role = params.get('role')
        tenant_id = params.get('tenant_id')
        user_id = params.get('user_id')

        # Fetch the token record from DynamoDB
        response = tokens_table.get_item(Key={'token': token})
        item = response.get('Item')

        if not item:
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Token no válido'})
            }

        # Si el rol es "admin", permitir tanto "role" como "tenant_id" y "user_id"
        if item['role'] == "admin":
            # Si se proporcionan ambos (role y tenant_id/user_id), validar los dos
            if role and (tenant_id or user_id):
                if role != item['role']:
                    return {
                        'statusCode': 403,
                        'body': json.dumps({'error': f'Token no válido para el role: {role}'})
                    }
                if tenant_id != item.get("tenant_id") or user_id != item.get("user_id"):
                    return {
                        'statusCode': 403,
                        'body': json.dumps({'error': 'Token no válido para el tenant_id y user_id proporcionados'})
                    }

            # Si solo se proporciona "role", validamos el role
            elif role:
                if role != item['role']:
                    return {
                        'statusCode': 403,
                        'body': json.dumps({'error': f'Token no válido para el role: {role}'})
                    }

            # Si solo se proporcionan "tenant_id" y "user_id", validamos estos
            elif tenant_id and user_id:
                if tenant_id != item.get("tenant_id") or user_id != item.get("user_id"):
                    return {
                        'statusCode': 403,
                        'body': json.dumps({'error': 'Token no válido para el tenant_id y user_id proporcionados'})
                    }

            # Si no se proporciona ni role ni tenant_id/user_id, devolver error
            else:
                return {
                    'statusCode': 400,
                    'body': json.dumps({'error': 'Debe enviar al menos role o tenant_id y user_id'})
                }
        # Check if the token has expired
        expires = datetime.strptime(item['expires'], '%Y-%m-%d %H:%M:%S')
        if datetime.utcnow() > expires:
            return {
                'statusCode': 403,
                'body': json.dumps({'error': 'Token expirado'})
            }

        # Token es válido
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Token válido'
            })
        }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
