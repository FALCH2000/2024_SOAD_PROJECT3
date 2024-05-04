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

def obtener_calendario_callback(message):
    # Procesa el mensaje recibido
    message = message.data.decode('utf-8')

    # convertir el mensaje a un diccionario
    message = json.loads(message)

    # json de respuesta
    mensaje = {}
    mensaje['available_tables'] = []

    # Obtener todas las mesas disponibles para una fecha y hora especifica

    try:
        # obtener todas las mesas
        mesas = usar_bd("SELECT * FROM Tables")

        # obtener las mesas ocupadas para esa fecha y hora
        mesas_ocupadas = usar_bd(f"SELECT * FROM Table_Availability WHERE Date_Reserved = '{message['date']}' AND Start_Time = '{message['hora']}'")
        if len(mesas_ocupadas) == 0:
            mensaje['available_tables'] = mesas
        else:
            # obtener las mesas disponibles 
            for mesa in mesas:
                if mesa not in mesas_ocupadas:
                    mensaje['available_tables'].append({"Table_ID": mesa[0], "Chairs" : mesa[1]})

        mensaje['status'] = 200
        mensaje['message'] = "Calendario obtenido correctamente"

    except Exception as e:
        mensaje['status'] = 500
        mensaje['message'] = f"Error al obtener el calendario: {str(e)}"

    # Convertir el mensaje a JSON
    mensaje_json = json.dumps(mensaje)
    
    # Publica el mensaje de confirmación en el mismo tema de Pub/Sub
    publisher = pubsub_v1.PublisherClient()
    topic_path = 'projects/groovy-rope-416616/topics/reserva'
    publisher.publish(topic_path, data=mensaje_json.encode(), type='obtener-calendario-resultado')
    
    # Marca el mensaje como confirmado
    message.ack()

def obtener_calendario(event, context):
    # Nombre de la suscripción a la que te quieres suscribir
    subscription_path = 'projects/groovy-rope-416616/subscriptions/obtener-calendario'

    # Suscribirse al tema
    future = subscriber.subscribe(subscription_path, callback=obtener_calendario_callback)
    print(f"Suscripto a la suscripción {subscription_path}")

    # Mantener la función en ejecución
    future.result()