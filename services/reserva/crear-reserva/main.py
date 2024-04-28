import json
from google.cloud import pubsub_v1

# Configura el cliente de Pub/Sub
subscriber = pubsub_v1.SubscriberClient()

def crear_reserva_callback(message):
    # Procesa el mensaje recibido
    reserva = message.data.decode('utf-8')

    # convertir el mensaje a un diccionario
    reserva = json.loads(reserva)

    mensaje = {}

    # revisar que reserva tenga los atributos correctos, la cantidad de atributos y que no estén vacíos
    if not all(key in reserva for key in ['id', 'fecha', 'hora', 'id_cliente', 'id_mesa']):
        print("La reserva no tiene los atributos correctos")
        mensaje = {
            "data": "No se pudo crear la reserva. La reserva no tiene los atributos correctos",
            "status": 200
        }
    else:
        ## verifica que haya disponibilidad de la mesa en la fecha y hora solicitada
        ## si no hay disponibilidad, se debe enviar un mensaje de error
        ## si hay disponibilidad, se debe guardar la reserva en la base de datos
        ## y enviar un mensaje de confirmación
        print("verificando disponibilidad de la mesa...")
        print("guardando reserva en la base de datos...")


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
    publisher.publish(topic_path, data=mensaje_json.encode(), type='crear-reserva-resultado')
    
    # Marca el mensaje como confirmado
    message.ack()


# entry point de la cloud function
def crear_reserva(event, context):
    # Nombre de la suscripción a la que te quieres suscribir
    subscription_path = 'CUAL'

    # Suscribirse al tema
    future = subscriber.subscribe(subscription_path, callback=crear_reserva_callback)
    print(f"Suscripto a la suscripción {subscription_path}")

    # Mantener la función en ejecución
    future.result()