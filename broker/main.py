import json
from google.cloud import pubsub_v1
import time

# Configura el cliente de Pub/Sub
subscriber = pubsub_v1.SubscriberClient()


def publish_message(topic, data, tipo):
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path("soa-project3", topic)
    data = data.encode("utf-8")
    attributes = {}
    attributes["type"] = tipo
    future = publisher.publish(topic_path, data=data, **attributes)
    print(future.result())



def get_topics():
    topics = {}
    topics["crear-reserva"] = "reserva"
    topics["editar-reserva"] = "reserva"
    topics["eliminar-reserva"] = "reserva"
    topics["ampliar-disponibilidad-reservas"] = "admin"
    topics["restablecer-password"] = "usuario"
    topics["crear-usuario"] = "usuario"
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

    request_json = request.get_json(silent=True)
    request_args = request.args
    path = (request.path)
    respuesta = {}
    print(f"Path: {path}, Method: {request.method}, Request: {request_json}, Args: {request_args}, Headers: {request.headers}")

    topics = get_topics()

    if request.method == "POST":
        if path == "/" and request_json["data"]["method"] == "crear-reserva":
            publish_message(topics["crear-reserva"], json.dumps(request_json), "crear-reserva")
            return ("Creando reserva...", 200, headers)
        elif path == "/" and request_json["data"]["method"] == "editar-reserva":
            publish_message(topics["editar-reserva"], json.dumps(request_json), "editar-reserva")
            return ("Editando reserva", 200, headers)
        elif path == "/" and request_json["data"]["method"] == "eliminar-reserva":
            publish_message(topics["eliminar-reserva"], json.dumps(request_json), "eliminar-reserva")
            return ("Eliminando reserva", 200, headers)
        elif path == "/" and request_json["data"]["method"] == "ampliar-disponibilidad-reservas":
            publish_message(topics["ampliar-disponibilidad-reservas"], json.dumps(request_json), "ampliar-disponibilidad-reservas")
            return ("Ampliando horario reservas", 200, headers)
        elif path == "/" and request_json["data"]["method"] == "restablecer-password":
            publish_message(topics["restablecer-password"], json.dumps(request_json), "restablecer-password")
            return ("Reestableciendo credenciales", 200, headers)
        elif path == "/" and request_json["data"]["method"] == "crear-usuario":
            publish_message(topics["crear-usuario"], json.dumps(request_json), "crear-usuario")
            return ("Creando usuario", 200, headers)
        else:
            respuesta = {
                "data": "",
                "status": 400,
                "message": "Bad Request. Metodo no valido"
            }
            return (json.dumps(respuesta), 400, headers)
    else:
        respuesta = {
            "data": "",
            "status": 400,
            "message": "Bad Request. Metodo no valido"
        }
        return (json.dumps(respuesta), 400, headers)