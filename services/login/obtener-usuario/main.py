import sqlalchemy
from google.cloud.sql.connector import Connector
import json
import jwt
from datetime import datetime, timedelta, timezone
import pytz
import hashlib

#Secret key to validate tokens
secret_key="6af00dfe63f6495195a3341ef6406c2c" 
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

def encriptar_texto(texto):
    # Codifica el texto en UTF-8 antes de encriptar
    texto_codificado = texto.encode('utf-8')
    # Crea un objeto hash utilizando el algoritmo SHA-256
    hash_obj = hashlib.sha256()
    # Actualiza el hash con el texto codificado
    hash_obj.update(texto_codificado)
    # Obtiene el hash en formato hexadecimal
    hash_str_hexadecimal = str(hash_obj.hexdigest())
    return hash_str_hexadecimal

def obtener_usuario_callback(username, password):
    respuesta = {}
    if username == "":
        respuesta["status"] = 400
        respuesta["message"] = "Error: No se ha ingresado un username."
        return respuesta
    encrypted_password = encriptar_texto(password)
    # Obtener datos del usuario
    user = usar_bd(F"SELECT * FROM User_ WHERE Username = '{username}' and {encrypted_password}")
    
    if user == []:
        respuesta["status"] = 404
        respuesta["message"] = "Error: Usuario no encontrado."
        respuesta["token"] = ""
        return respuesta
    
    token = jwt.encode(
        payload={
            "user": username,
            "password": password,
            "exp": str(datetime.now(timezone.utc)+ timedelta(seconds= 600))
        },
        key=secret_key
    )
    respuesta["status"] = 200

    respuesta["message"] = "Usuario encontrado."

    respuesta["token"] = token

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
    print(request_args)
    # Set CORS headers for main requests
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
    }

    if path == "/" and request.method == 'GET' and request_args.get('username') != "" and  request_args.get('password') != "":
        return (obtener_usuario_callback(request_args('username'),request_args('password')),200,headers)
    else:
        respuesta["status"] = 404
        respuesta["message"] = f"Error: Método no válido."
        return (f"{json.dumps(respuesta, ensure_ascii=True)}",400,headers)