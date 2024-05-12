import sqlalchemy
from google.cloud.sql.connector import Connector
import json
from datetime import datetime, timezone
import pytz
import hashlib
import jwt

# REVISAR SCRIPT DE CREACION DE LA BASE DE DATOS ANTES DE PROGRAMAR CUALQUIER QUERY
# Este metodo es REST

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
secret_key="6af00dfe63f6495195a3341ef6406c2c" 
def token_invalido(token):
    try:
        token_decoded  = jwt.decode(jwt=token, key=secret_key)
    except jwt.ExpiredSignatureError:
        return False



def verificar_usuario_callback(request):
    respuesta = {}
    #verificar el token
    try:
        token_decoded  = jwt.decode(jwt=request.args.get('token'), key=secret_key)
    except jwt.ExpiredSignatureError:
        respuesta["status"] = 401
        respuesta["message"] = "Error: EL TOKEN esta expirado!"
        return json.dumps(respuesta, ensure_ascii=False)
    except jwt.exceptions.InvalidTokenError as e:
        respuesta["status"] = 401
        respuesta["message"] = "Error: EL TOKEN no es valido!"
        return json.dumps(respuesta, ensure_ascii=False)
    except Exception as e:
        respuesta["status"] = 500
        respuesta["message"] = "Error: procesando el token"
        return json.dumps(respuesta, ensure_ascii=False)
    
    # verificar datos del usuario
    username = token_decoded['username']
    password = encriptar_texto(token_decoded['password'])
    if username == "" or password == "":
        respuesta["status"] = 400
        respuesta["message"] = "Error: No se ha ingresado un username o password."
        return json.dumps(respuesta, ensure_ascii=False)
    
    # Verificar contrasena del usuario
    user = usar_bd(F"SELECT * FROM User_ WHERE Username = '{username}' AND Encrypted_Password = '{password}'")
    if user == []:
        respuesta["status"] = 404
        respuesta["message"] = "Error: Usuario no existe o la contrasena es incorrecta."
        return json.dumps(respuesta, ensure_ascii=False)

    respuesta["status"] = 200
    respuesta["message"] = "Usuario encontrado."
    return json.dumps(respuesta)

def verificar_usuario(request):
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
    #and request_json is None and not request_args
    if path == "/" and request.method == 'GET':
        return (verificar_usuario_callback(request_args('token')),200,headers)
    else:
        respuesta["status"] = 404
        respuesta["message"] = "Error: Método no válido."
        return (f"{json.dumps(respuesta, ensure_ascii=False)}",404,headers)