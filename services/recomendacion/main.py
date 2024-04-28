import json
from google.cloud import pubsub_v1

# Configura el cliente de Pub/Sub
subscriber = pubsub_v1.SubscriberClient()

def obtener_recomendacion_callback(message):
    # Procesa el mensaje recibido
    recomendacion = message.data.decode('utf-8')

    # convertir el mensaje a un diccionario
    recomendacion = json.loads(recomendacion)

    mensaje = {}

    # revisar que recomendación tenga los atributos correctos, la cantidad de atributos y que no estén vacíos
    if not all(key in recomendacion for key in ['id', 'fecha', 'hora', 'id_cliente', 'id_mesa']):
        print("La reserva no tiene los atributos correctos")
        mensaje = {
            "data": "No se pudo obtener una recomendación. No tiene los atributos correctos",
            "status": 200
        }
    else:
        ## verifica si existe alguna recomendación con los platos indicados
        ## si no existe, se envía un mensaje de error
        ## si existe, se envía un mensaje de éxito
        print("Buscando recomendación...")


    # Mensaje de confirmación como un diccionario
    mensaje = {
        "data": "Reserva creada con éxito",
        "status": 201
    }
    
    # Convertir el mensaje a JSON
    mensaje_json = json.dumps(mensaje)
    
    # Publica el mensaje de confirmación en el mismo tema de Pub/Sub
    publisher = pubsub_v1.PublisherClient()
    topic_path = 'CAMBIAR'
    publisher.publish(topic_path, data=mensaje_json.encode(), type='obtener-recomendacion-resultado')
    
    # Marca el mensaje como confirmado
    message.ack()


# entry point de la cloud function
def obtener_recomendacion(event, context):
    # Nombre de la suscripción a la que te quieres suscribir
    subscription_path = 'CUAL'

    # Suscribirse al tema
    future = subscriber.subscribe(subscription_path, callback=obtener_recomendacion_callback)
    print(f"Suscripto a la suscripción {subscription_path}")

    # Mantener la función en ejecución
    future.result()