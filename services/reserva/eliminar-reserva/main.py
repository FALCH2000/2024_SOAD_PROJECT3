import sqlalchemy
from google.cloud.sql.connector import Connector
import json
from google.cloud import pubsub_v1
import datetime
import pytz

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
    # Marca el mensaje como confirmado
    message.ack()

    # json de respuesta
    mensaje = {}

    # Definir la zona horaria US-Central
    us_central_tz = pytz.timezone('US/Central')

    # Obtener la hora actual en la zona horaria US-Central
    hora_actual_us_central = datetime.datetime.now(us_central_tz)

    # Convertir a la zona horaria de Arizona
    zona_horaria_arizona = pytz.timezone('US/Arizona')
    hora_actual_arizona = hora_actual_us_central.astimezone(zona_horaria_arizona)

    hora_actual = hora_actual_us_central.strftime('%H:%M:%S')
    fecha_actual = hora_actual_us_central.strftime('%Y-%m-%d')

    print("Hora actual en Arizona:", hora_actual_arizona)
    print("Hora normal en Arizona:", hora_actual)

    if  not all(key in reservaporborrar['data'] for key in ['method', 'reservation_id', 'username', 'reservation_date', 'start_time']):
        mensaje['status'] = '400'
        mensaje['message'] = 'Faltan datos en la solicitud'
        return mensaje
    
    elif reservaporborrar['data']['method'] == "eliminar-reserva":
        try:

            # verificar si la reserva es futura
            if fecha_actual > reservaporborrar['data']['reservation_date']:
                mensaje['status'] = '400'
                mensaje['message'] = 'No se puede eliminar una reserva pasada'
                return mensaje
            
            # obtener las mesas asociadas a la reserva
            mesasporliberar = usar_bd(f"SELECT Table_ID FROM Reservation_Tables_Association WHERE Reservation_ID = {reservaporborrar['data']['reservation_id']}")
            print(f"mesasporliberar = {mesasporliberar}")  # [#row][#column]
            
            delete_from_db(f"DELETE FROM Reservation_Tables_Association WHERE Reservation_ID = {reservaporborrar['data']['reservation_id']}")
            
            # liberar las mesas ocupadas
            for row in mesasporliberar:
                delete_from_db(f"DELETE FROM Table_Availability WHERE Table_ID = {str(row[0])} \
                            AND Date_Reserved = '{reservaporborrar['data']['reservation_date']}' \
                            AND Start_Time = '{reservaporborrar['data']['start_time']}'")
            
            delete_from_db(f"DELETE FROM Reservations WHERE Reservation_ID = {reservaporborrar['data']['reservation_id']}")
            
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

def eliminar_reserva(event, context):
    # Nombre de la suscripción a la que te quieres suscribir
    subscription_path = 'projects/groovy-rope-416616/subscriptions/eliminar-reserva'

    # Suscribirse al tema
    future = subscriber.subscribe(subscription_path, callback=eliminar_reserva_callback)
    print(f"Suscripto a la suscripción {subscription_path}")

    # Mantener la función en ejecución
    future.result()