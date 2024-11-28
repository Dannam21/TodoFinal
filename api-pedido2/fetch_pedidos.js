const AWS = require("aws-sdk");
const dynamoDB = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    const { email } = event.queryStringParameters || {};
    const params = {
        TableName: "Pedidos",
        KeyConditionExpression: "email = :email",
        ExpressionAttributeValues: { ":email": email },
    };

    try {
        const data = await dynamoDB.query(params).promise();
        return { statusCode: 200, body: JSON.stringify(data.Items) };
    } catch (error) {
        return { statusCode: 500, body: JSON.stringify({ message: "Error al consultar pedidos", error }) };
    }
};
