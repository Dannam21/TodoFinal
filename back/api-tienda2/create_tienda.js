const AWS = require("aws-sdk");
const dynamoDB = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    let body;
    
    if (typeof event.body === 'string') {
        body = JSON.parse(event.body);
    } else {
        body = event.body;
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
        return { statusCode: 201, body: JSON.stringify({ message: "Tienda creada" }) };
    } catch (error) {
        return { statusCode: 500, body: JSON.stringify({ message: "Error al crear tienda", error }) };
    }
};
