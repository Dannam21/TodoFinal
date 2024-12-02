const AWS = require("aws-sdk");
const dynamoDB = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    let body;

    if (typeof event.body === "string") {
        body = JSON.parse(event.body); // Si el body es un string, lo parseamos
    } else {
        body = event.body; // Si ya es un objeto, usamos el cuerpo tal cual
    }

    const { resena_id, tenant_id, contenido, puntuacion } = body;

    const params = {
        TableName: process.env.RESENA_TABLE,  // Usamos la variable de entorno para el nombre de la tabla
        Item: {
            resena_id,           // ID de la reseña (podrías generar un UUID o usar un identificador único)
            tenant_id,           // ID del tenant (si aplica)
            contenido,           // Contenido de la reseña
            puntuacion,          // Puntuación de la reseña
            fechaCreacion: new Date().toISOString(),  // Fecha de creación de la reseña
        },
    };

    try {
        // Insertamos el item en la tabla DynamoDB
        await dynamoDB.put(params).promise();
        return { statusCode: 201, body: JSON.stringify({ message: "Reseña creada con éxito" }) };
    } catch (error) {
        // Si ocurre algún error, devolvemos un error 500
        return { statusCode: 500, body: JSON.stringify({ message: "Error al crear la reseña", error }) };
    }
};
