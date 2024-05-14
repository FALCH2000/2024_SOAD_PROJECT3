import json
from google.cloud import pubsub_v1
import time

# Configura el cliente de Pub/Sub
subscriber = pubsub_v1.SubscriberClient()

def publish_message(topic, data, tipo):
    print("Publishing message")
    publisher = pubsub_v1.PublisherClient()
    # topic_path = publisher.topic_path("soa-project3", topic)
    data = data.encode("utf-8")  # Convertir a JSON y luego a bytestring
    print(f"data: {data}")
    
    print(f"Publishing message to {topic} with data")
    future = publisher.publish(topic, data=data, type=tipo)
    print(future.result())


def get_topics():
    topics = {}
    topics["crear-reserva"] = "projects/soa-project3/topics/reserva"
    topics["editar-reserva"] = "projects/soa-project3/topics/reserva"
    topics["eliminar-reserva"] = "projects/soa-project3/topics/reserva"
    topics["ampliar-disponibilidad-reservas"] = "projects/soa-project3/topics/admin"
    topics["restablecer-password"] = "projects/soa-project3/topics/usuario"
    topics["crear-usuario"] = "projects/soa-project3/topics/usuario"
    return topics

# entry point de la cloud function
def broker(request):
    if request.method == "OPTIONS":
        # Allows GET requests from any origin with the Content-Type
        # header and caches preflight response for an 3600s
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET",
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Max-Age": "3600",
        }

        return ("", 204, headers)
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
    }

    print("Request: ", request)
    request_json = request.get_json(silent=True)
    request_args = request.args
    path = (request.path)
    respuesta = {}
    print(f"Path: {path}, Method: {request.method}, Request: {request_json}, Args: {request_args}, Headers: {request.headers}")

    topics = get_topics()

    if request.method == "POST":
        try:
            if path == "/" and request_json["data"]["method"] == "crear-reserva":
                publish_message(topics["crear-reserva"], json.dumps(request_json), "crear-reserva")
                return (json.dumps({"response" : "Reserva creada"}), 200, headers)
            elif path == "/" and request_json["data"]["method"] == "editar-reserva":
                publish_message(topics["editar-reserva"], json.dumps(request_json), "editar-reserva")
                return (json.dumps({"response" : "Reserva editada"}), 200, headers)
            elif path == "/" and request_json["data"]["method"] == "eliminar-reserva":
                publish_message(topics["eliminar-reserva"], json.dumps(request_json), "eliminar-reserva")
                return (json.dumps({"response" : "Reserva eliminada"}), 200, headers)
            elif path == "/" and request_json["data"]["method"] == "ampliar-disponibilidad-reservas":
                publish_message(topics["ampliar-disponibilidad-reservas"], json.dumps(request_json), "ampliar-disponibilidad-reservas")
                return (json.dumps({"response" : "Se amplio el horario disponible"}), 200, headers)
            elif path == "/" and request_json["data"]["method"] == "restablecer-password":
                publish_message(topics["restablecer-password"], json.dumps(request_json), "restablecer-password")
                return (json.dumps({"response" : "Contrasena reestablecida"}), 200, headers)
            elif path == "/" and request_json["method"] == "crear-usuario":
                publish_message(topics["crear-usuario"], request_json, "crear-usuario")
                return (json.dumps({"response" : "Usuario creado"}), 200, headers)
            else:
                respuesta = {
                    "data": "",
                    "status": 400,
                    "message": "Bad Request. Metodo no valido"
                }
                return (json.dumps(respuesta), 400, headers)
        except Exception as e:
            respuesta = {
                "data": "",
                "status": 400,
                "message": "Error: " + str(e)
            }
            return (json.dumps(respuesta), 400, headers)
    else:
        respuesta = {
            "data": "",
            "status": 400,
            "message": "Bad Request. Metodo no valido"
        }
        return (json.dumps(respuesta), 400, headers)