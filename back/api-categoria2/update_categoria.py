import boto3
import os
import logging
import json

# Inicialización de recursos
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

def lambda_handler(event, context):
    try:
        # Verifica si el cuerpo de la solicitud está presente
        if not event.get('body'):
            logger.error("No se proporcionó cuerpo de solicitud")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'El cuerpo de la solicitud es requerido'})
            }
        
        body = json.loads(event['body'])  # Suponemos que el cuerpo está en formato JSON
        
        # Obtener los parámetros necesarios
        tenant_id = body.get('tenant_id')
        categoria_id = body.get('categoria_id')
        nombre = body.get('nombre')
        
        # Validación de parámetros
        if not tenant_id or not categoria_id or not nombre:
            logger.error("Faltan parámetros obligatorios: tenant_id, categoria_id o nombre")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'tenant_id, categoria_id y nombre son obligatorios'})
            }

        logger.info(f"Actualizando categoría: tenant_id={tenant_id}, categoria_id={categoria_id}, nombre={nombre}")
        
        # Realizar la actualización en DynamoDB
        response = table.update_item(
            Key={'tenant_id': tenant_id, 'categoria_id': categoria_id},
            UpdateExpression="SET nombre = :nombre",
            ExpressionAttributeValues={':nombre': nombre},
            ReturnValues="ALL_NEW"
        )

        # Obtener los atributos actualizados
        updated_item = response.get('Attributes', None)
        
        if not updated_item:
            logger.warning(f"No se encontró la categoría con tenant_id={tenant_id} y categoria_id={categoria_id}")
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Categoría no encontrada'})
            }

        logger.info(f"Categoría actualizada: {updated_item}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({'categoria_actualizada': updated_item})  # Convertimos a JSON
        }

    except json.JSONDecodeError:
        logger.error("Error al decodificar el cuerpo de la solicitud: formato JSON incorrecto")
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Cuerpo de la solicitud debe ser un JSON válido'})
        }
    
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f"Error interno del servidor: {str(e)}"})
        }
