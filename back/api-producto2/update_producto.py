import boto3
import os
import json

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Deserializar el cuerpo si es una cadena JSON
        body = json.loads(event['body']) if isinstance(event['body'], str) else event['body']

        tenant_id = body.get('tenant_id')
        producto_id = body.get('producto_id')
        updates = body.get('updates')

        if not tenant_id or not producto_id or not updates:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'tenant_id, producto_id y updates son requeridos'})
            }

        update_expression = "SET "
        expression_values = {}

        # Construir la expresión de actualización
        for key, value in updates.items():
            update_expression += f" {key} = :{key},"
            expression_values[f":{key}"] = value

        # Eliminar la última coma de la expresión
        update_expression = update_expression.rstrip(',')

        # Realizar la actualización en DynamoDB
        response = table.update_item(
            Key={'tenant_id': tenant_id, 'producto_id': producto_id},
            UpdateExpression=update_expression,
            ExpressionAttributeValues=expression_values,
            ReturnValues="ALL_NEW"
        )

        # Devolver la respuesta con los atributos actualizados
        return {
            'statusCode': 200
        }

    except Exception as e:
        # Manejo de errores
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f'Error al actualizar el producto: {str(e)}'})
        }
