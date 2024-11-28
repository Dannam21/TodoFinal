const AWS = require("aws-sdk");
const dynamoDB = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    const { tenantID, tiendaID } = event.queryStringParameters || {};
    const params = {
        TableName: "Productos",
        KeyConditionExpression: "tenantID = :tenantID AND tiendaID = :tiendaID",
        ExpressionAttributeValues: {
            ":tenantID": tenantID,
            ":tiendaID": tiendaID,
        },
    };

    try {
        const data = await dynamoDB.query(params).promise();
        return { statusCode: 200, body: JSON.stringify(data.Items) };
    } catch (error) {
        return { statusCode: 500, body: JSON.stringify({ message: "Error al consultar producto", error }) };
    }
};
