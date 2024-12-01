import boto3
import os
import logging
import json
from decimal import Decimal

# Configuración de logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


# Función para convertir objetos Decimal a tipos JSON serializables
def decimal_to_str(obj):
    """Convierte recursivamente cualquier objeto Decimal a su valor serializable JSON."""
    if isinstance(obj, Decimal):
        return float(obj) if obj % 1 else int(obj)  # Convierte Decimal a float o int
    elif isinstance(obj, dict):
        return {k: decimal_to_str(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [decimal_to_str(i) for i in obj]
    else:
        return obj


def lambda_handler(event, context):
    try:
        # Obtén el nombre de la tabla desde las variables de entorno
        table_name = os.environ.get('TABLE_NAME', 'DefaultTable')
        logger.info(f"Nombre de la tabla: {table_name}")

        # Accede a los parámetros queryStringParameters
        tenant_id = event['queryStringParameters'].get('tenant_id', None)
        categoria_nombre = event['queryStringParameters'].get('categoria_nombre', None)
        producto_id = event['queryStringParameters'].get('producto_id', None)

        # Verificar si todos los parámetros requeridos están presentes
        if not tenant_id or not categoria_nombre or not producto_id:
            logger.error("Faltan parámetros requeridos: tenant_id, categoria_nombre o producto_id")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'tenant_id, categoria_nombre y producto_id son obligatorios'})
            }

        logger.info(
            f"Parámetros recibidos - tenant_id: {tenant_id}, categoria_nombre: {categoria_nombre}, producto_id: {producto_id}")

        # Crear el recurso DynamoDB
        dynamodb = boto3.resource('dynamodb')

        # Obtener la tabla de DynamoDB usando el nombre de la tabla
        table = dynamodb.Table(table_name)

        # Realizar la consulta utilizando la clave de partición 'tenant_id#categoria_nombre' y la clave de ordenación 'producto_id'
        response = table.query(
            KeyConditionExpression=boto3.dynamodb.conditions.Key('tenant_id').eq(tenant_id) &
                                   boto3.dynamodb.conditions.Key('producto_id').eq(producto_id)
        )

        # Revisar los resultados de la consulta
        logger.info(f"Respuesta de DynamoDB: {json.dumps(response, indent=2)}")

        # Buscar el producto específico dentro de los resultados
        item = None
        for i in response.get('Items', []):
            if i['producto_id'] == producto_id:
                item = i
                break

        if not item:
            logger.info(
                f"Producto no encontrado para tenant_id: {tenant_id}, categoria_nombre: {categoria_nombre} y producto_id: {producto_id}")
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Producto no encontrado'})
            }

        # Convertir los valores de Decimal a tipos JSON serializables antes de devolver la respuesta
        item = decimal_to_str(item)

        logger.info(f"Producto encontrado: {item}")

        # Responder con el producto encontrado
        return {
            'statusCode': 200,
            'body': json.dumps({'producto': item})  # Convertimos el item a JSON
        }

    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f"Error interno del servidor: {str(e)}"})
        }
