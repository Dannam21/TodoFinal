const AWS = require("aws-sdk");
const dynamoDB = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    const { tenantID, tiendaID, nombre, precio } = JSON.parse(event.body);
    const params = {
        TableName: "Productos",
        Item: {
            tenantID,
            tiendaID,
            nombre,
            precio,
            fechaCreacion: new Date().toISOString(),
        },
    };

    try {
        await dynamoDB.put(params).promise();
        return { statusCode: 201, body: JSON.stringify({ message: "Producto creado" }) };
    } catch (error) {
        return { statusCode: 500, body: JSON.stringify({ message: "Error al crear producto", error }) };
    }
};
