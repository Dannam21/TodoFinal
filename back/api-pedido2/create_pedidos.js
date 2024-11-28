const AWS = require("aws-sdk");
const dynamoDB = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    const { email, nombre, password } = JSON.parse(event.body);
    const params = {
        TableName: "Pedidos",
        Item: { email, nombre, password, createdAt: new Date().toISOString() },
    };

    try {
        await dynamoDB.put(params).promise();
        return { statusCode: 201, body: JSON.stringify({ message: "Pedido creado" }) };
    } catch (error) {
        return { statusCode: 500, body: JSON.stringify({ message: "Error al crear pedido", error }) };
    }
};
