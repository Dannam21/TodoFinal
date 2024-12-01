import boto3
import os
import logging
import json

def lambda_handler(event, context):
    try:
        # Obtén el nombre de la tabla desde las variables de entorno
        table_name = os.environ.get('TABLE_NAME', 'DefaultTable') 
        logging.info(f"Nombre de la tabla: {table_name}")
        
        # Accede a los parámetros queryStringParameters
        tenant_id = event['queryStringParameters'].get('tenant_id', None)
        categoria_nombre = event['queryStringParameters'].get('categoria_nombre', None)
        producto_id = event['queryStringParameters'].get('producto_id', None)
        
        # Verificar si todos los parámetros requeridos están presentes
        if not tenant_id or not categoria_nombre or not producto_id:
            logging.error("Faltan parámetros requeridos: tenant_id, categoria_nombre o producto_id")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'tenant_id, categoria_nombre y producto_id son obligatorios'})
            }

        logging.info(f"Parámetros recibidos - tenant_id: {tenant_id}, categoria_nombre: {categoria_nombre}, producto_id: {producto_id}")
        
        # Crear el recurso DynamoDB
        dynamodb = boto3.resource('dynamodb')
        
        # Obtener la tabla de DynamoDB usando el nombre de la tabla
        table = dynamodb.Table(table_name)
        
        # Crear la clave de partición usando tenant_id#categoria_nombre
        partition_key = f"{tenant_id}#{categoria_nombre}"
        
        # Loguear las claves que estamos usando
        logging.info(f"Clave de partición: {partition_key}")
        logging.info(f"Producto ID: {producto_id}")

        # Ejecutar la consulta en la tabla para obtener el producto por producto_id
        response = table.get_item(
            Key={
                'tenant_id#categoria_nombre': partition_key,
                'producto_id': producto_id
            }
        )

        # Obtener el item de la respuesta
        item = response.get('Item', None)

        if not item:
            logging.info(f"Producto no encontrado para tenant_id: {tenant_id}, categoria_nombre: {categoria_nombre} y producto_id: {producto_id}")
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Producto no encontrado'})
            }

        logging.info(f"Producto encontrado: {item}")

        return {
            'statusCode': 200,
            'body': json.dumps({'producto': item})  # Convertimos el item a JSON
        }
    
    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f"Error interno del servidor: {str(e)}"})
        }
