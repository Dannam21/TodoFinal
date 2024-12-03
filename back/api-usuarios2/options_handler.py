def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',  # Permitir cualquier origen
            'Access-Control-Allow-Methods': 'GET, POST, PATCH, PUT, DELETE, OPTIONS',  # Métodos permitidos
            'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Amz-Security-Token',  # Encabezados permitidos
            'Access-Control-Allow-Credentials': 'false',  # Puedes poner true si necesitas credenciales
        },
        'body': ''
    }
