import json
from google.cloud import pubsub_v1

# Configura el cliente de Pub/Sub
subscriber = pubsub_v1.SubscriberClient()

# Lista para almacenar las reservas
mis_reservas = []

def callback(message):
    global mis_reservas
    # Procesa el mensaje recibido
    reserva = message.data.decode('utf-8')
    mis_reservas.append(reserva)
    
    # Mensaje de confirmación como un diccionario
    mensaje = {
        "data": "Reserva creada con éxito",
        "status": 201
    }
    
    # Convertir el mensaje a JSON
    mensaje_json = json.dumps(mensaje)
    
    # Publica el mensaje de confirmación en el mismo tema de Pub/Sub
    publisher = pubsub_v1.PublisherClient()
    topic_path = 'projects/proyecto3soa-421620/topics/generar-reserva'
    publisher.publish(topic_path, data=mensaje_json.encode(), k1='crear-nueva-reserva-resultado')
    
    # Marca el mensaje como confirmado
    message.ack()
# entry point de la cloud function
def suscribirse_a_suscripcion(event, context):
    # Nombre de la suscripción a la que te quieres suscribir
    subscription_path = 'projects/proyecto3soa-421620/subscriptions/crear-reserva'
    
    # Suscribirse al tema
    future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Suscripto a la suscripción {subscription_path}")

    # Mantener la función en ejecución
    future.result()
