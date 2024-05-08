import sqlalchemy
from google.cloud.sql.connector import Connector
import json
import datetime
import pytz

# REVISAR SCRIPT DE CREACION DE LA BASE DE DATOS ANTES DE PROGRAMAR CUALQUIER QUERY
# Este metodo es REST y al ser de tipo GET por ende si devuelve algo

# Obtains data from database
def getconn():
    connector = Connector()
    conn = connector.connect(
        "groovy-rope-416616:us-central1:database-project3",
        "pytds",
        user="sqlserver",
        password="4321",
        db="restaurant-db"
    )
    return conn

# Creates a connection pool to the database
def get_engine():
    pool = sqlalchemy.create_engine(
        "mssql+pytds://",
        creator=getconn,
    )
    return pool

# Can perform SELECTS and return data
def usar_bd(solicitud):
    conn = get_engine().connect()
    result = conn.execute(solicitud)
    data = []  # Create an empty list to store data
    for row in result:
        print(f"row = {row}")
        data.append(row)  # Append each row to the list
    conn.close()
    return data  # Return the captured data

# Can perform INSERTS, UPDATES, DELETES, etc. but does not return data
def usar_bd_sin_return(solicitud):
    conn = get_engine().connect()
    conn.execute(solicitud)
    conn.close()

def obtener_usuario_callback(username):
    respuesta = {}

    if username == "":
        respuesta["status"] = 400
        respuesta["message"] = "Error: No se ha ingresado un username."
        return respuesta

    # Obtener datos del usuario
    user = usar_bd(F"SELECT * FROM User_ WHERE Username = '{username}'")

    if user == []:
        respuesta["status"] = 404
        respuesta["message"] = "Error: Usuario no encontrado."
        return respuesta
    
    respuesta["status"] = 200
    respuesta["message"] = "Usuario encontrado."

    return json.dumps(respuesta)


# entry point de la cloud function
def obtener_usuario(request):

    # Set CORS headers for the preflight request
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

    request_json = request.get_json(silent=True)
    request_args = request.args
    path = (request.path)
    respuesta = {}

    # Set CORS headers for main requests
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
    }

    if path == "/" and request.method == 'GET' and request_args.get('username') != "":
        return (obtener_usuario_callback(request_args('username')),200,headers)
    else:
        respuesta["status"] = 404
        respuesta["message"] = "Error: Método no válido."
        return (f"{json.dumps(respuesta, ensure_ascii=False)}",404,headers)