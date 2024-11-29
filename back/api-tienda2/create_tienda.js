const AWS = require("aws-sdk");
const dynamoDB = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    let body;

    // If the event body is already an object (parsed), use it directly
    if (typeof event.body === "string") {
        body = JSON.parse(event.body); // Parse if it's a string
    } else {
        body = event.body; // Otherwise, assume it's already an object
    }

    const { tenant_id, datos } = body;

    const params = {
        TableName: "Tienda",
        Item: {
            tenant_id,
            datos,
            fechaCreacion: new Date().toISOString(),
        },
    };

    try {
        await dynamoDB.put(params).promise();
        return { statusCode: 201, body: JSON.stringify({ message: "Tienda creado" }) };
    } catch (error) {
        return { statusCode: 500, body: JSON.stringify({ message: "Error al crear tienda", error }) };
    }
};
