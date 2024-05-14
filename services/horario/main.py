import sqlalchemy
from google.cloud.sql.connector import Connector
import json
from google.cloud import pubsub_v1
from datetime import datetime
import time

# Configura el cliente de Pub/Sub
subscriber = pubsub_v1.SubscriberClient()

# Obtains all data from database
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

def insert_into_db(solicitud):
    conn = get_engine().connect()
    conn.execute(solicitud)
    conn.close()



def ampliar_disponibilidad_reservas_callback(message):
    try:
        # Procesa el mensaje recibido
        datos_restaurante = json.loads(message.data.decode('utf-8'))

        # Verifica que todos los datos necesarios estén presentes
        required_fields = ['Local_ID', 'Opening_Time', 'Closing_Time']
        if not all(field in datos_restaurante for field in required_fields):
            print("El mensaje no contiene todos los datos necesarios")
            message.ack()
            return

        # Obtener los datos del restaurante de la base de datos
        local_id = datos_restaurante['Local_ID']
        query = f"SELECT Opening_Time, Closing_Time FROM Restaurant_Data WHERE Local_ID = {local_id}"
        data = usar_bd(query)
        
        if not data:
            print(f"No se encontraron datos para el restaurante con ID {local_id}")
            message.ack()
            return
        
        # Verificar si los horarios de apertura y cierre son válidos
        opening_time = datetime.strptime(datos_restaurante['Opening_Time'], '%H:%M:%S').time()
        closing_time = datetime.strptime(datos_restaurante['Closing_Time'], '%H:%M:%S').time()
        current_opening_time = data[0]['Opening_Time']
        current_closing_time = data[0]['Closing_Time']

        print(f"Horarios actuales: {current_opening_time} - {current_closing_time}")
        print(f"Horarios nuevos: {opening_time} - {closing_time}")

        print(f"horario actual >= horario nuevo: {current_opening_time >= opening_time}")
        print(f"horario actual <= horario nuevo: {closing_time >= current_closing_time}")

        if current_opening_time >= opening_time and closing_time >= current_closing_time:
            # Actualizar la disponibilidad de reservas
            query = f"UPDATE Restaurant_Data SET Opening_Time = '{opening_time}', Closing_Time = '{closing_time}' WHERE Local_ID = {local_id}"
            insert_into_db(query)
            print(f"Se actualizó la disponibilidad de reservas del restaurante con ID {local_id}")
        else:
            print(f"Los horarios de apertura y cierre no son válidos para el restaurante con ID {local_id}")
    
    except Exception as e:
        print("Ocurrió un error:", e)
    
    # Marca el mensaje como confirmado
    message.ack()



# entry point de la cloud function
def ampliar_disponibilidad_reservas(event, context):
    # Nombre de la suscripción a la que te quieres suscribir
    subscription_path = 'projects/soa-project3/subscriptions/ampliar-disponibilidad-reservas'

    # Suscribirse al tema
    future = subscriber.subscribe(subscription_path, callback=ampliar_disponibilidad_reservas_callback)
    print(f"Suscripto a la suscripción {subscription_path}")

    # Mantener la función en ejecución
    future.result()