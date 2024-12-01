const AWS = require("aws-sdk");
const uuid = require("uuid");
const dynamodb = new AWS.DynamoDB.DocumentClient();
const TABLE_NAME = process.env.TABLE_NAME;

const crearResenia = async (event) => {
    try {
        const body = typeof event.body === "string" ? JSON.parse(event.body) : event.body;

        const { tenant_id, producto_id, usuario_id, puntaje, comentario } = body;

        // Validación de datos
        if (!tenant_id || !producto_id || !usuario_id || !puntaje || !comentario) {
            return {
                statusCode: 400,
                body: JSON.stringify({ message: "Datos incompletos" })
            };
        }

        if (puntaje < 1 || puntaje > 5) {
            return {
                statusCode: 400,
                body: JSON.stringify({ message: "El puntaje debe estar entre 1 y 5" })
            };
        }

        const resenia_id = uuid.v4();
        const resenia = {
            tenant_id,
            resenia_id,
            producto_id,
            usuario_id,
            detalle: {
                puntaje,
                comentario
            }
        };

        const params = {
            TableName: TABLE_NAME,
            Item: resenia
        };

        await dynamodb.put(params).promise();

        return {
            statusCode: 201,
            body: JSON.stringify({ message: "Reseña creada exitosamente", resenia })
        };
    } catch (error) {
        console.error("Error al insertar la reseña en DynamoDB:", error);
        return {
            statusCode: 500,
            body: JSON.stringify({ message: "Error al crear la reseña", error: error.message })
        };
    }
};

// Exportar la función
module.exports.crearResenia = crearResenia;
