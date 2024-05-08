import sqlalchemy
from google.cloud.sql.connector import Connector
import json
from google.cloud import pubsub_v1
import datetime
import pytz
import hashlib

# REVISAR SCRIPT DE CREACION DE LA BASE DE DATOS ANTES DE PROGRAMAR CUALQUIER QUERY
# Este metodo utiliza pub/sub, y por ello no es igual a un metodo REST

# Configura el cliente de Pub/Sub
subscriber = pubsub_v1.SubscriberClient()

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

def crear_usuario_callback(message):
    request = message.data.decode('utf-8')
    request = json.loads(request) # dictionary
    message.ack()

    # Verificar que la solicitud contenga todos los datos necesarios
    if not all(key in request for key in ['username', 'password', 'first_name', 'last_name1', 'last_name2', 'security_question', 'security_answer']):
        print("Codigo: 400. Faltan datos en la solicitud de creacion de usuario.")
        return
    
    # Verificar que el metodo sea correcto
    if request['method'] != "crear-usuario":
        print("Codigo: 400. Metodo incorrecto.")
        return

    try:
        # Encriptar la contraseña
        encrypted_password = encriptar_texto(request['password'])
        encrypted_security_question = encriptar_texto(request['security_question'])
        encrypted_security_answer = encriptar_texto(request['security_answer'])

        # Crear la solicitud SQL
        usar_bd_sin_return(f"INSERT INTO User_ (Username, Encrypted_Password, First_Name, Last_Name1, Last_Name2, Security_Question, Security_Answer) \
                        VALUES ('{request['username']}', '{encrypted_password}', '{request['first_name']}', '{request['last_name1']}', \
                        '{request['last_name2']}', '{encrypted_security_question}', '{encrypted_security_answer}')")
        
        print("Codigo: 200. Usuario creado exitosamente.")
    
    except Exception as e:
        print(f"Codigo: 500. Error al crear el usuario: {e}")

def crear_usuario(event, context):
    # Nombre de la suscripcion a la que te quieres suscribir
    subscription_path = 'projects/groovy-rope-416616/subscriptions/crear-usuario'

    # Suscribirse
    future = subscriber.subscribe(subscription_path, callback=crear_usuario_callback)
    print(f"Suscrito a la suscripción {subscription_path}")

    # Mantener la función en ejecución
    future.result()