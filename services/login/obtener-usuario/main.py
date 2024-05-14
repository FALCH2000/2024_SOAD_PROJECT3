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
        "soa-project3:us-central1:database-project3",
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

def obtener_usuario_callback(username, password, headers):
    """
    Verifies the request and retrieves the user information.

    Args:
        username (str): The username provided in the request.
        password (str): The password provided in the request.
        headers (dict): The headers of the request.

    Returns:
        tuple: A tuple containing the JSON response, status code, and headers.
    """

    print("Verificando request")

    respuesta = {}
    if username == "":
        respuesta["status"] = 400
        respuesta["message"] = "Error: No se ha ingresado un username."
        return (json.dumps(respuesta), respuesta["status"], headers)
    
    print("Username ingresado correctamente")

    encrypted_password = encriptar_texto(password)

    # Obtener datos del usuario
    user = usar_bd(F"SELECT * FROM User_ WHERE Username = '{username}' and Encrypted_Password = '{encrypted_password}'")

    if user == []:
        respuesta["status"] = 404
        respuesta["message"] = "Error: Usuario no encontrado."
        
        return (json.dumps(respuesta), respuesta["status"], headers)

    print("El usuario si existe. Se procedera a generar el token del usuario: ", username)

    type = usar_bd(f"SELECT Type_ID FROM User_Type_Association WHERE Username='{username}'")

    if type[0] == 1:
        type = "admin"
    else:
        type = "client"

    print("El tipo de usuario es: ", type)

    # Calcular la fecha de expiración como un entero de tiempo Unix en segundos
    exp_timestamp = int((datetime.now(timezone.utc) + timedelta(seconds=1800)).timestamp()) # 1800 segundos = 30 minutos

    token = jwt.encode(
        payload={   
            "username": username,
            "password": password,
            "exp": exp_timestamp
        },
        key=secret_key,
    )

    print("Token generado correctamente")

    respuesta["token"] = token
    respuesta["type"] = type
    respuesta["status"] = 200
    respuesta["message"] = "Usuario encontrado y token generado."

    return (json.dumps(respuesta), respuesta["status"], headers)

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

    print("BREAKPOINT ENTRY POINT PARA OBTENER USUARIO")

    if path == "/" and request.method == 'GET' and request_args.get('username') != "" and  request_args.get('password') != "":
        #return obtener_usuario_callback(request_args('username'),request_args('password'), headers)
        return obtener_usuario_callback(request_args['username'], request_args['password'], headers)

    else:
        respuesta["status"] = 404
        respuesta["message"] = f"Error: Método no válido."
        return (f"{json.dumps(respuesta)}",400,headers)