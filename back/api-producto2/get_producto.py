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

        # Validar parámetros
        if not producto_id:
            logging.error("Falta el parámetro requerido: producto_id")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'producto_id es obligatorio'})
            }

        logging.info(f"Parámetro recibido - producto_id: {producto_id}")
        
        # Crear el recurso DynamoDB
        dynamodb = boto3.resource('dynamodb')
        
        # Obtener la tabla de DynamoDB usando el nombre de la tabla
        table = dynamodb.Table(table_name)
        
        # Ejecutar la consulta en la tabla con la clave primaria (producto_id)
        response = table.get_item(
            Key={
                'producto_id': producto_id
            }
        )

        # Obtener el item de la respuesta
        item = response.get('Item', None)

        if not item:
            logging.info(f"Producto no encontrado para producto_id: {producto_id}")
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
