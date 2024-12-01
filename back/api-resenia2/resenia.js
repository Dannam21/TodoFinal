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

        // Generar el ID de la reseña
        const resenia_id = uuid.v4();

        // Crear el atributo combinado tenant_id_producto_id
        const tenant_id_producto_id = `${tenant_id}#${producto_id}`;

        // Crear el objeto de la reseña
        const resenia = {
            tenant_id,
            producto_id,
            resenia_id,
            usuario_id,
            detalle: {
                puntaje,
                comentario
            },
            tenant_id_producto_id,  // Esto no es necesario en KeySchema, solo lo guardamos aquí
            fecha: new Date().toISOString() // Se puede usar para indexar por fecha si es necesario
        };

        const params = {
            TableName: TABLE_NAME,
            Item: resenia
        };

        // Guardar la reseña en DynamoDB
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
