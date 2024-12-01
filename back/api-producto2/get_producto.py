import boto3
import os
import logging
import json

# Configuración de logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

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

        logger.info(f"Parámetros recibidos - tenant_id: {tenant_id}, categoria_nombre: {categoria_nombre}, producto_id: {producto_id}")
        
        # Crear el recurso DynamoDB
        dynamodb = boto3.resource('dynamodb')
        
        # Obtener la tabla de DynamoDB usando el nombre de la tabla
        table = dynamodb.Table(table_name)

        # Realizar la consulta usando el índice global (GSI) con 'precio'
        response = table.query(
            IndexName="GSI_TenantID_Precio",  # Consultamos usando el GSI con 'precio' como clave de ordenamiento
            KeyConditionExpression=boto3.dynamodb.conditions.Key('tenant_id').eq(tenant_id) & boto3.dynamodb.conditions.Key('precio').eq(producto_id)  # O la condición que desees
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
            logger.info(f"Producto no encontrado para tenant_id: {tenant_id}, categoria_nombre: {categoria_nombre} y producto_id: {producto_id}")
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Producto no encontrado'})
            }

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
