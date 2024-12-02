const AWS = require('aws-sdk');
const dynamoDb = new AWS.DynamoDB.DocumentClient();

const TABLE_NAME = process.env.TABLE_NAME;

// Crear reseña
module.exports.crearResena = async (event) => {
    const { tenant_id, producto_id, resenia_id, fecha, datos } = JSON.parse(event.body);

    const params = {
        TableName: TABLE_NAME,
        Item: {
            'tenant_id#producto_id': `${tenant_id}#${producto_id}`,
            resenia_id,
            fecha,
            datos,
        },
    };

    try {
        await dynamoDb.put(params).promise();
        return {
            statusCode: 201,
            body: JSON.stringify({ message: 'Reseña creada exitosamente' }),
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Error al crear la reseña', details: error.message }),
        };
    }
};

// Obtener reseñas por producto
module.exports.obtenerResenas = async (event) => {
    const { tenant_id, producto_id } = event.pathParameters;

    const params = {
        TableName: TABLE_NAME,
        KeyConditionExpression: 'tenant_id#producto_id = :key',
        ExpressionAttributeValues: {
            ':key': `${tenant_id}#${producto_id}`,
        },
    };

    try {
        const result = await dynamoDb.query(params).promise();
        return {
            statusCode: 200,
            body: JSON.stringify(result.Items),
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Error al obtener reseñas', details: error.message }),
        };
    }
};

// Actualizar reseña
module.exports.actualizarResena = async (event) => {
    const { tenant_id, producto_id, resenia_id, datos } = JSON.parse(event.body);

    const params = {
        TableName: TABLE_NAME,
        Key: {
            'tenant_id#producto_id': `${tenant_id}#${producto_id}`,
            resenia_id,
        },
        UpdateExpression: 'set datos = :datos',
        ExpressionAttributeValues: {
            ':datos': datos,
        },
        ReturnValues: 'UPDATED_NEW',
    };

    try {
        const result = await dynamoDb.update(params).promise();
        return {
            statusCode: 200,
            body: JSON.stringify({ message: 'Reseña actualizada', data: result.Attributes }),
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Error al actualizar la reseña', details: error.message }),
        };
    }
};

// Eliminar reseña
module.exports.eliminarResena = async (event) => {
    const { tenant_id, producto_id, resenia_id } = JSON.parse(event.body);

    const params = {
        TableName: TABLE_NAME,
        Key: {
            'tenant_id#producto_id': `${tenant_id}#${producto_id}`,
            resenia_id,
        },
    };

    try {
        await dynamoDb.delete(params).promise();
        return {
            statusCode: 200,
            body: JSON.stringify({ message: 'Reseña eliminada exitosamente' }),
        };
    } catch (error) {
        return {
            statusCode: 500,
            body: JSON.stringify({ error: 'Error al eliminar la reseña', details: error.message }),
        };
    }
};
