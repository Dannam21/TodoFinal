const AWS = require("aws-sdk");
const dynamoDB = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    const { resena_id } = event.queryStringParameters;  // Si se pasa un ID de reseña en los parámetros

    const params = {
        TableName: process.env.RESENA_TABLE,
        Key: {
            resena_id,  // Usamos el ID de la reseña como la clave principal
        },
    };

    try {
        const result = await dynamoDB.get(params).promise();
        if (!result.Item) {
            return { statusCode: 404, body: JSON.stringify({ message: "Reseña no encontrada" }) };
        }
        return { statusCode: 200, body: JSON.stringify(result.Item) };
    } catch (error) {
        return { statusCode: 500, body: JSON.stringify({ message: "Error al obtener la reseña", error }) };
    }
};
