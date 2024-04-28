from google.cloud import pubsub_v1
import json
# Configura el cliente de Pub/Sub
publisher = pubsub_v1.PublisherClient()

# Define el tema y los mensajes con sus respectivos atributos
topic_path = 'projects/proyecto3soa-421620/topics/generar-reserva'
mensaje_crear_reserva = {
    'data': 'Contenido del mensaje para crear una reserva',
    'attributes': {'k1': 'crear-nueva-reserva'}
}
mensaje_obtener_resultado = {
    'data': 'Contenido del mensaje para obtener el resultado de una reserva',
    'attributes': {'k1': 'crear-nueva-reserva-resultado'}
}

# Codifica los mensajes como bytes
mensaje_crear_reserva_bytes = json.dumps(mensaje_crear_reserva).encode('utf-8')
mensaje_obtener_resultado_bytes = json.dumps(mensaje_obtener_resultado).encode('utf-8')

# Publica los mensajes en el tema con los respectivos atributos
future = publisher.publish(topic_path, data=mensaje_crear_reserva_bytes, k1='crear-nueva-reserva')
publisher.publish(topic_path, data=mensaje_obtener_resultado_bytes, k1='crear-nueva-reserva-resultado')

print(f"futuro: {future.result()}")
print("Mensajes publicados correctamente en el tema.")
