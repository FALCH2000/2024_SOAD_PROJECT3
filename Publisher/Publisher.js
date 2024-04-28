const { PubSub } = require('@google-cloud/pubsub');
const pubSubClient = new PubSub();
const topicNameOrId = 'projects/proyecto3soa-421620/topics/generar-reserva';
const mensaje = {
    "data": "Crea una reserva",
    "id": "1",
    "tipo": "crear-reserva",
    "fecha": "2021-10-29",
    "hora": "10:00",
    "idCliente": "1",
    "idMesa": "1",
    "idRestaurante": "1"
  };
  const data = JSON.stringify(mensaje);
  

async function publishMessage(topicNameOrId, data) {
  const dataBuffer = Buffer.from(data);
  const customAttributes = {
    k1: 'crear-nueva-reserva',
  };

  try {
    // Publica el mensaje en el tema
    const messageId = await pubSubClient
      .topic(topicNameOrId)
      .publishMessage({data: dataBuffer, attributes: customAttributes});

    console.log(`Mensaje ${messageId} publicado.`);

    // Suscribirse a un tema donde se publicará la respuesta del suscriptor
    const subscriptionName = 'obtener-resultado-crear-reserva'; // Reemplazar con el nombre de tu suscripción
    const subscription = pubSubClient.subscription(subscriptionName);

    // Escuchar mensajes de la suscripción
    subscription.on('message', messageHandler);
  } catch (error) {
    console.error(`Error al publicar el mensaje: ${error.message}`);
    process.exitCode = 1;
  }
}

async function messageHandler(message) {
  try {
    // Manejar la respuesta del suscriptor
    console.log(`Mensaje recibido: ${message.id}`);
    console.log(`Contenido del mensaje: ${message.data.toString()}`);
    
    // Marcar el mensaje como confirmado
    message.ack();
  } catch (error) {
    console.error(`Error al manejar el mensaje: ${error.message}`);
  }
}

publishMessage(topicNameOrId, data);
