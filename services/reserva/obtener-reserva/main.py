import sqlalchemy
from google.cloud.sql.connector import Connector
import json
from google.cloud import pubsub_v1

# Configura el cliente de Pub/Sub
subscriber = pubsub_v1.SubscriberClient()

# Obtains all data from database
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

# Test function to test connection to database
def usar_bd(solicitud):
    conn = get_engine().connect()
    result = conn.execute(solicitud)
    data = []  # Create an empty list to store data
    for row in result:
        print(f"row = {row}")
        data.append(row)  # Append each row to the list
    conn.close()
    return data  # Return the captured data

def obtener_reserva_callback(message):
    # Procesa el mensaje recibido
    reservaporobtener = message.data.decode('utf-8')

    # convertir el mensaje a un diccionario
    reservaporobtener = json.loads(reservaporobtener)

    # json de respuesta
    mensaje = {}

def obtener_reserva(event, context):
    # Nombre de la suscripción a la que te quieres suscribir
    subscription_path = 'projects/groovy-rope-416616/subscriptions/obtener-reserva'

    # Suscribirse al tema
    future = subscriber.subscribe(subscription_path, callback=obtener_reserva_callback)
    print(f"Suscripto a la suscripción {subscription_path}")

    # Mantener la función en ejecución
    future.result()
