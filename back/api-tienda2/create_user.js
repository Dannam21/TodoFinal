const AWS = require("aws-sdk");
const dynamoDB = new AWS.DynamoDB.DocumentClient();

exports.handler = async (event) => {
    const { tenant_id, email, nombre, passwordHash } = JSON.parse(event.body);
    const params = {
        TableName: "Usuarios",
        Item: {
            tenant_id,
            email,
            nombre,
            passwordHash,
            fechaCreacion: new Date().toISOString(),
        },
    };

    try {
        await dynamoDB.put(params).promise();
        return { statusCode: 201, body: JSON.stringify({ message: "Usuario creado" }) };
    } catch (error) {
        return { statusCode: 500, body: JSON.stringify({ message: "Error al crear usuario", error }) };
    }
};