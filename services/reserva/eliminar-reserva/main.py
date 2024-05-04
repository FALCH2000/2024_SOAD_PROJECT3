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

def delete_from_db(solicitud):
    conn = get_engine().connect()
    conn.execute(solicitud)
    conn.close()

def eliminar_reserva_callback(message):
    # Procesa el mensaje recibido
    reservaporborrar = message.data.decode('utf-8')

    # convertir el mensaje a un diccionario
    reservaporborrar = json.loads(reservaporborrar)

    # json de respuesta
    mensaje = {}

    print(f" Id mesa: {reservaporborrar['data']['reserved_tables']['table_id']}")

    # Eliminar la reserva
    try:
        delete_from_db(f"DELETE FROM Reservation_Tables_Association WHERE Reservation_ID = {reservaporborrar['data']['reservation_id']}")
        delete_from_db(f"DELETE FROM Reservations WHERE Reservation_ID = {reservaporborrar['data']['reservation_id']}")
        delete_from_db(f"DELETE FROM Table_Availability \
                        WHERE Table_ID = {reservaporborrar['data']['reserved_tables']['table_id']} \
                        AND Date_Reserved = '{reservaporborrar['data']['reservation_date']}' \
                        AND Start_Time = '{reservaporborrar['data']['start_time']}'")

        mensaje['status'] = '200'
        mensaje['message'] = 'Reserva eliminada'
    except Exception as e:
        mensaje['status'] = '500'
        mensaje['message'] = f'Error al eliminar la reserva: {str(e)}'

    # Convertir el mensaje a JSON
    mensaje_json = json.dumps(mensaje)
    
    # Publica el mensaje de confirmación en el mismo tema de Pub/Sub
    publisher = pubsub_v1.PublisherClient()
    topic_path = 'projects/groovy-rope-416616/topics/reserva'
    publisher.publish(topic_path, data=mensaje_json.encode(), type='eliminar-reserva-resultado')
    
    # Marca el mensaje como confirmado
    message.ack()

def eliminar_reserva(event, context):
    # Nombre de la suscripción a la que te quieres suscribir
    subscription_path = 'projects/groovy-rope-416616/subscriptions/eliminar-reserva'

    # Suscribirse al tema
    future = subscriber.subscribe(subscription_path, callback=eliminar_reserva_callback)
    print(f"Suscripto a la suscripción {subscription_path}")

    # Mantener la función en ejecución
    future.result()