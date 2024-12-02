const AWS = require("aws-sdk");
const { v4: uuidv4 } = require("uuid"); // Para generar resenia_id

const dynamoDB = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    let body;

    // Parsear el cuerpo de la solicitud
    if (typeof event.body === "string") {
        body = JSON.parse(event.body);
    } else {
        body = event.body;
    }

    // Extraer los campos del cuerpo
    const { tenant_id, producto_id, datos } = body;

    // Validar que los campos obligatorios estén presentes
    if (!tenant_id || !producto_id || !datos) {
        return {
            statusCode: 400,
            body: JSON.stringify({ message: "Faltan campos obligatorios (tenant_id, producto_id o datos)." }),
        };
    }

    // Generar los valores autogenerados
    const resenia_id = uuidv4(); // Identificador único para la reseña
    const fecha = new Date().toISOString(); // Fecha actual en formato ISO

    // Parámetros para guardar en DynamoDB
    const params = {
        TableName: process.env.RESENIAS_TABLE, // Usar variable de entorno para el nombre de la tabla
        Item: {
            tenant_id_producto_id: `${tenant_id}#${producto_id}`, // Clave de partición
            resenia_id, // Clave de ordenamiento
            fecha, // Fecha de creación
            datos, // Información de la reseña
        },
    };

    try {
        // Guardar en DynamoDB
        await dynamoDB.put(params).promise();
        return {
            statusCode: 201,
            body: JSON.stringify({
                message: "Reseña creada exitosamente",
                resenia: params.Item,
            }),
        };
    } catch (error) {
        console.error("Error al guardar la reseña:", error);
        return {
            statusCode: 500,
            body: JSON.stringify({ message: "Error al crear la reseña", error }),
        };
    }
};
