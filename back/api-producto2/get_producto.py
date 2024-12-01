import boto3
import os
import json
from boto3.dynamodb.conditions import Key

# Configuración de logging
dynamodb = boto3.resource('dynamodb')
table_name = os.environ['TABLE_NAME']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # Obtener los parámetros de la consulta
        params = event.get('queryStringParameters', {})
        tenant_id = params.get('tenant_id')
        categoria_nombre = params.get('categoria_nombre')
        producto_id = params.get('producto_id')  # Optional parameter

        # Verificar si los parámetros requeridos están presentes
        if not tenant_id or not categoria_nombre:
            return {
                'statusCode': 400,
                'body': json.dumps({'message': 'tenant_id y categoria_nombre son obligatorios'})
            }

        # Registrar los parámetros recibidos para auditoría
        print(f"Parámetros recibidos - tenant_id: {tenant_id}, categoria_nombre: {categoria_nombre}, producto_id: {producto_id}")

        # Preparar la consulta en función de los parámetros recibidos
        key_condition = Key('tenantID').eq(tenant_id) & Key('categoria_nombre').eq(categoria_nombre)
        
        # Si producto_id está presente, agregar un filtro
        filter_expression = None
        if producto_id:
            filter_expression = Key('producto_id').eq(producto_id)

        # Ejecutar la consulta usando el GSI
        response = table.query(
            IndexName='GSI_TenantID_CategoriaNombre',  # Nombre del índice GSI
            KeyConditionExpression=key_condition,
            FilterExpression=filter_expression,  # Si producto_id está presente, lo usamos
            ProjectionExpression='producto_id, nombre, stock'  # Ajusta los atributos según lo necesario
        )

        # Obtener los ítems de la respuesta
        items = response.get('Items', [])
        print(f"Items encontrados: {items}")  # Imprime los ítems encontrados para verificar

        if not items:
            # Si no hay productos encontrados, retornar un mensaje adecuado
            return {
                'statusCode': 404,
                'body': json.dumps({'message': 'No se encontraron productos'})
            }

        # Si se encuentran productos, retornar los datos
        return {
            'statusCode': 200,
            'body': json.dumps({'productos': items})
        }
    
    except Exception as e:
        # Capturar cualquier excepción y retornar un error 500
        print(f"Error inesperado: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'message': f"Error interno del servidor: {str(e)}"})
        }
