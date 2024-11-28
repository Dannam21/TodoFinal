const AWS = require("aws-sdk");
const dynamoDB = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    const { email, nombre, password } = JSON.parse(event.body);
    const params = {
        TableName: "Pedidos",
        Key: { email },
        UpdateExpression: "set nombre = :nombre, password = :password",
        ExpressionAttributeValues: { ":nombre": nombre, ":password": password },
        ReturnValues: "UPDATED_NEW",
    };

    try {
        const result = await dynamoDB.update(params).promise();
        return { statusCode: 200, body: JSON.stringify({ message: "Pedido actualizado", result }) };
    } catch (error) {
        return { statusCode: 500, body: JSON.stringify({ message: "Error al actualizar pedido", error }) };
    }
};
