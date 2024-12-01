import boto3
import os
import logging
import json

# Configuración de logging
logging.basicConfig(level=logging.INFO)

def lambda_handler(event, context):
    try:
        # Obtén el nombre de la tabla desde las variables de entorno
        table_name = os.environ.get('TABLE_NAME', 'DefaultTable')
        logging.info(f"Nombre de la tabla: {table_name}")
        
        # Accede a los parámetros queryStringParameters
        producto_id = event['queryStringParameters'].get('producto_id', None)
        tenant_id = event['queryStringParameters'].get('tenant_id', None)
        categoria_nombre = event['queryStringParameters'].get('categoria_nombre', None)

        # Validar parámetros
        if not producto_id or not tenant_id or not categoria_nombre:
            logging.error("Faltan parámetros requeridos: producto_id, tenant_id o categoria_nombre")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'producto_id, tenant_id y categoria_nombre son obligatorios'})
            }

        logging.info(f"Parámetros recibidos - producto_id: {producto_id}, tenant_id: {tenant_id}, categoria_nombre: {categoria_nombre}")
        
        # Crear el recurso DynamoDB
        dynamodb = boto3.resource('dynamodb')
        
        # Obtener la tabla de DynamoDB usando el nombre de la tabla
        table = dynamodb.Table(table_name)
        
        # Crear la clave de partición
        partition_key = f"{tenant_id}#{categoria_nombre}"

        # Ejecutar la consulta en la tabla
        response = table.get_item(
            Key={
                'tenant_id#categoria_nombre': partition_key,
                'producto_id': producto_id
            }
        )

        # Obtener el item de la respuesta
        item = response.get('Item', None)

        if not item:
            logging.info(f"Producto no encontrado para tenant_id: {tenant_id}, categoria_nombre: {categoria_nombre}, producto_id: {producto_id}")
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'Producto no encontrado'})
            }

        logging.info(f"Producto encontrado: {item}")

        # Retornar el producto encontrado
        return {
            'statusCode': 200,
            'body': json.dumps({'producto': item})  # Convertimos a JSON
        }
    
    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f"Error interno del servidor: {str(e)}"})
        }
