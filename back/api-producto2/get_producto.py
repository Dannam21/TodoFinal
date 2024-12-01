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
        print(table)

        # Realizar la consulta usando el índice global (GSI)
        response = table.query(
            IndexName="GSI_TenantID_CategoriaNombre",  # Asegúrate de que el nombre del índice sea correcto
            KeyConditionExpression=boto3.dynamodb.conditions.Key('tenantID').eq(tenant_id) & boto3.dynamodb.conditions.Key('categoria_nombre').eq(categoria_nombre),
            FilterExpression=boto3.dynamodb.conditions.Key('producto_id').eq(producto_id)  # Filtrar por producto_id
        )

        print(response)
        print(item)
        
        for i in response.get('Items', []):
            if i['producto_id'] == producto_id:
                item = i
                break

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
