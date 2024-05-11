import sqlalchemy
from google.cloud.sql.connector import Connector
import json
from google.cloud import pubsub_v1
import datetime
import pytz
import hashlib


# REVISAR SCRIPT DE CREACION DE LA BASE DE DATOS ANTES DE PROGRAMAR CUALQUIER QUERY
# Este metodo utiliza pub/sub, y por ello no es igual a un metodo REST
# Este metodo se encarga de cambiar la contrasena de un usuario al cual se le olvido su contrasena actual
# No devuelve nada, pero imprime en consola el resultado de la operacion


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

def cambiar_contrasena_callback(message):
    request = message.data.decode('utf-8')
    request = json.loads(request) # dictionary
    message.ack()
    if not all(key in request for key in ['method', 'username', "new_password", "security_answer"]):
        print("Codigo: 400. Faltan atributos en la solicitud para cambiar contrasena.")
        return
    
    if request['method'] == "cambiar-contrasena":
        try:
            # Verify if the user exists
            user = usar_bd(f"SELECT * FROM User_ WHERE Username = '{request['username']}'")
            if user == []:
                print(f"Codigo: 400. El usuario {request['username']} no existe.")
                return
            
            # Verify is the user answered correctly the security question
            stored_security_answer = usar_bd(f"SELECT Security_Answer FROM User_ WHERE Username = '{request['username']}'")
            current_answer_encrypted = encriptar_texto(request['security_answer'])
            
            if stored_security_answer[0][0] != current_answer_encrypted:
                print("Could not verify security Awnsers")
                print(f"Codigo: 400. La respuesta de seguridad es incorrecta.")
                return
            
            # Update the user's password
            usar_bd_sin_return(f"UPDATE User_ SET Encrypted_Password = '{encriptar_texto(request['new_password'])}' \
                               WHERE username = '{request['username']}'")
            
            print(f"Codigo: 200. Se ha cambiado la contrasena del usuario {request['username']} exitosamente.")
            
        except Exception as err:
            print(f"Codigo: 500. Error: {err}")

def cambiar_contrasena(event, context):
    # Nombre de la suscripcion a la que te quieres suscribir
    subscription_path = "projects/groovy-rope-416616/subscriptions/restablecer-password"

    # Suscribirse
    future = subscriber.subscribe(subscription_path, callback=cambiar_contrasena_callback)
    print(f"Suscrito a la suscripción {subscription_path}")

    # Mantener la función en ejecución
    future.result()