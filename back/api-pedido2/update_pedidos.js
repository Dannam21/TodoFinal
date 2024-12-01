const AWS = require("aws-sdk");
const dynamoDB = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    const { tenant_id, producto_id, pedido_id, estado } = JSON.parse(event.body);
    const tenantID_productoID = tenant_id + "#" + producto_id;

    const params = {
        TableName: process.env.PEDIDOS_TABLE,
        Key: { 'tenant_id#producto_id': tenantID_productoID,
                'pedido_id': pedido_id},
        UpdateExpression: "set estado = :estado",
        ExpressionAttributeValues: { ":estado": estado },
        ReturnValues: "UPDATED_NEW",
    };

    try {
        const result = await dynamoDB.update(params).promise();
        return { statusCode: 200, body: JSON.stringify({ message: "Pedido actualizado", result }) };
    } catch (error) {
        return { statusCode: 500, body: JSON.stringify({ message: "Error al actualizar pedido", error }) };
    }
};
