const AWS = require("aws-sdk");
const dynamoDB = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    const { email } = JSON.parse(event.body);
    const params = {
        TableName: "Pedidos",
        Key: { email },
    };

    try {
        await dynamoDB.delete(params).promise();
        return { statusCode: 200, body: JSON.stringify({ message: "Pedido eliminado" }) };
    } catch (error) {
        return { statusCode: 500, body: JSON.stringify({ message: "Error al eliminar pedido", error }) };
    }
};
