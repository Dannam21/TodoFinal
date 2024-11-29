const AWS = require("aws-sdk");
const dynamoDB = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    const { tenant_id, email } = event.queryStringParameters || {};
    const params = {
        TableName: "Usuarios",
        KeyConditionExpression: "tenant_id = :tenant_id AND email = :email",
        ExpressionAttributeValues: {
            ":tenant_id": tenant_id,
            ":email": email,
        },
    };

    try {
        const data = await dynamoDB.query(params).promise();
        return { statusCode: 200, body: JSON.stringify(data.Items) };
    } catch (error) {
        return { statusCode: 500, body: JSON.stringify({ message: "Error al consultar usuario", error }) };
    }
};