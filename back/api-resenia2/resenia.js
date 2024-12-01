const AWS = require("aws-sdk");
const uuid = require("uuid");
const dynamodb = new AWS.DynamoDB.DocumentClient();
const TABLE_NAME = process.env.TABLE_NAME;

const crearResenia = async (event) => {
    try {
        const body = typeof event.body === "string" ? JSON.parse(event.body) : event.body;
        const { tenant_id, producto_id, usuario_id, puntaje, comentario } = body;

        if (!tenant_id || !producto_id || !usuario_id || !puntaje || !comentario) {
            return {
                statusCode: 400,
                body: JSON.stringify({ message: "Datos incompletos" })
            };
        }

        const resenia_id = uuid.v4();

        // Crear el atributo combinado tenant_id_producto_id en la Lambda
        const tenant_id_producto_id = `${tenant_id}#${producto_id}`;

        const resenia = {
            tenant_id,
            producto_id,
            resenia_id,
            usuario_id,
            detalle: {
                puntaje,
                comentario
            },
            tenant_id_producto_id,  // Solo lo guardamos aquí, no en el KeySchema de DynamoDB
            fecha: new Date().toISOString()  // Puede ser útil si necesitas indexar por fecha
        };

        const params = {
            TableName: TABLE_NAME,
            Item: resenia
        };

        await dynamodb.put(params).promise();

        return {
            statusCode: 200,
            body: JSON.stringify({ message: "Reseña creada exitosamente", resenia })
        };
    } catch (error) {
        console.error(error);
        return {
            statusCode: 500,
            body: JSON.stringify({ message: "Error al crear la reseña", error: error.message })
        };
    }
};

module.exports.crearResenia = crearResenia;
