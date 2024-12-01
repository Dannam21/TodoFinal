const AWS = require("aws-sdk");
const dynamoDB = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    const { tenant_id, producto_id, pedido_id } = JSON.parse(event.body);
    const tenantID_productoID = tenant_id + "#" + producto_id;

    const params = {
        TableName: process.env.PEDIDOS_TABLE,
        Key: {
            'tenant_id#producto_id': tenantID_productoID,
            'pedido_id': pedido_id
        },
    };

    try {
        await dynamoDB.delete(params).promise();
        return { statusCode: 204, body: JSON.stringify({ message: "Pedido eliminado" }) };
    } catch (error) {
        return { statusCode: 500, body: JSON.stringify({ message: "Error al eliminar pedido", error }) };
    }
};
