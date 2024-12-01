const AWS = require("aws-sdk");
const dynamoDB = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    const { tenant_id, usuario_id, datos } = JSON.parse(event.body);
    const producto_id = crypto.randomUUID();
    const estado = "PENDIENTE";

    if (!tenant_id || !usuario_id || !datos) {
        return {
            statusCode: 400,
            body: JSON.stringify({
                error: 'Missing required data (tenant_id, usuario_id, datos)'
            })
        };
    }

    const params = {
        TableName: process.env.PEDIDOS_TABLE,
        Item: { tenant_id, producto_id, usuario_id,
                estado,
                datos,
                createdAt: new Date().toISOString() },
    };

    try {
        await dynamoDB.put(params).promise();
        return { statusCode: 201, body: JSON.stringify({ message: "Pedido creado" }) };
    } catch (error) {
        console.error("Error creating order:", error);
        return { statusCode: 500, body: JSON.stringify({ message: "Error al crear pedido", error }) };
    }
};
