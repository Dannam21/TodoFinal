const AWS = require("aws-sdk");
const { v4: uuidv4 } = require("uuid"); // Para generar resenia_id

const dynamoDB = new AWS.DynamoDB.DocumentClient();

module.exports.createResenia = async (event) => {
  try {
    // Parseamos el cuerpo de la solicitud
    const { tenant_id, producto_id, datos } = JSON.parse(event.body);

    // Validamos que los campos requeridos estén presentes
    if (!tenant_id || !producto_id || !datos) {
      return {
        statusCode: 400,
        body: JSON.stringify({ message: "Faltan campos obligatorios." }),
      };
    }

    // Generamos resenia_id y fecha automáticamente
    const resenia_id = uuidv4(); // Genera un identificador único
    const fecha = new Date().toISOString(); // Fecha en formato ISO 8601

    // Creamos el objeto que se guardará en DynamoDB
    const item = {
      tenant_id_producto_id: `${tenant_id}#${producto_id}`, // Clave de partición
      resenia_id, // Clave de ordenamiento
      fecha, // Fecha autogenerada
      datos, // Datos de la reseña
    };

    // Guardamos en DynamoDB
    await dynamoDB
      .put({
        TableName: "ReseniasTable", // Cambia por el nombre de tu tabla
        Item: item,
      })
      .promise();

    // Retornamos la respuesta
    return {
      statusCode: 201,
      body: JSON.stringify({
        message: "Reseña creada exitosamente.",
        resenia: item,
      }),
    };
  } catch (error) {
    console.error("Error creando la reseña:", error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        message: "Error interno al crear la reseña.",
      }),
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
