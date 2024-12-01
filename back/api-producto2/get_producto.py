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
        tenant_id = event['queryStringParameters'].get('tenant_id', None)
        categoria_nombre = event['queryStringParameters'].get('categoria_nombre', None)

        # Validar parámetros
        if not tenant_id or not categoria_nombre:
            logging.error("Faltan parámetros requeridos: tenant_id o categoria_nombre")
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'tenant_id y categoria_nombre son obligatorios'})
            }

        logging.info(f"Parámetros recibidos - tenant_id: {tenant_id}, categoria_nombre: {categoria_nombre}")
        
        # Crear el recurso DynamoDB
        dynamodb = boto3.resource('dynamodb')
        
        # Obtener la tabla de DynamoDB usando el nombre de la tabla
        table = dynamodb.Table(table_name)
        
        # Ejecutar la consulta usando el GSI
        response = table.query(
            IndexName='GSI_TenantID_CategoriaNombre',
            KeyConditionExpression='tenantID = :tenant_id and categoria_nombre = :categoria_nombre',
            ExpressionAttributeValues={
                ':tenant_id': tenant_id,
                ':categoria_nombre': categoria_nombre
            }
        )

        # Obtener los ítems de la respuesta
        items = response.get('Items', [])

        if not items:
            logging.info(f"No se encontraron productos para tenant_id: {tenant_id} y categoria_nombre: {categoria_nombre}")
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'No se encontraron productos'})
            }

        logging.info(f"Productos encontrados: {items}")

        # Retornar los productos encontrados
        return {
            'statusCode': 200,
            'body': json.dumps({'productos': items})  # Convertimos a JSON
        }
    
    except Exception as e:
        logging.error(f"Error inesperado: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f"Error interno del servidor: {str(e)}"})
        }
