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

def insert_into_db(solicitud):
    conn = get_engine().connect()
    conn.execute(solicitud)
    conn.close()

def crear_reserva_callback(message):
    # Procesa el mensaje recibido
    reserva = message.data.decode('utf-8')

    # convertir el mensaje a un diccionario
    reserva = json.loads(reserva)

    # json de respuesta
    mensaje = {}
    mensaje['data'] = {}
    mensaje['data']['reservation_id'] = ""
    mensaje['data']['tables'] = []

    # revisar que reserva tenga los atributos correctos, la cantidad de atributos y que no estén vacíos
    if not all(key in reserva['data'] for key in ['method', 'username', 'number_of_people', 'reservation_date', 'start_time', 'end_time', 'selected_tables']):
        mensaje = {
            "data": "",
            "status": 400,
            "message": "Bad Request. Faltaron atributos para crear la reserva"
        }
    elif reserva['data']['method'] == "crear-reserva":
        ## TODO: verificar que haya disponibilidad de la mesa en la fecha y hora solicitada
        ## si no hay disponibilidad, se debe enviar un mensaje de error
        ## si hay disponibilidad, se debe guardar la reserva en la base de datos
        ## y enviar un mensaje de confirmación
        
        # Se asume que hay disponibilidad de las mesas seleccionadas
        # Guardar la reserva en la base de datos
        insert_into_db(f"INSERT INTO Reservations (User_ID, Number_Of_People, Date_Reserved, Start_Time, End_Time)\
                VALUES ('{reserva['data']['username']}', {reserva['data']['number_of_people']}, \
                '{reserva['data']['reservation_date']}', '{reserva['data']['start_time']}', \
                '{reserva['data']['end_time']}')")
        
        reservation_id = usar_bd(f"SELECT Reservation_ID FROM Reservations \
                                 WHERE User_ID = '{reserva['data']['username']}' \
                                AND Date_Reserved = '{reserva['data']['reservation_date']}' \
                                AND Start_Time = '{reserva['data']['start_time']}' \
                                AND End_Time = '{reserva['data']['end_time']}'")
        
        # La hora de fin de la reserva es dos horas despues de la hora de inicio
        

        # Guardar la disponibilidad de las mesas en la base de datos
        for table_id in reserva['data']['selected_tables']:
            insert_into_db(f"INSERT INTO Table_Availability (Table_ID, Date_Reserved, Start_Time, End_Time) \
                    VALUES ({table_id}, '{reserva['data']['reservation_date']}', '{reserva['data']['start_time']}', \
                    '{reserva['data']['end_time']}')")
            
            # Guardar la asociacion entre la reserva y las mesas seleccionadas
            insert_into_db(f"INSERT INTO Reserved_Tables (Reservation_ID, Table_ID) \
                    VALUES ({reservation_id}, {table_id})")
        

        # Mensaje de confirmación como un diccionario
        mensaje['data']['reservation_id'].append(reservation_id)
        mensaje['data']['tables'].append(reserva['data']['selected_tables'])

        mensaje['status'] = 200
        mensaje['message'] = "OK. Reserva creada exitosamente"
    
    else:
        mensaje = {
            "data": "",
            "status": 400,
            "message": "Bad Request. Metodo no valido"
        }

    # Convertir el mensaje a JSON
    mensaje_json = json.dumps(mensaje)
    
    # Publica el mensaje de confirmación en el mismo tema de Pub/Sub
    publisher = pubsub_v1.PublisherClient()
    topic_path = 'projects/groovy-rope-416616/topics/reserva'
    publisher.publish(topic_path, data=mensaje_json.encode(), type='crear-reserva-resultado')
    
    # Marca el mensaje como confirmado
    message.ack()


# entry point de la cloud function
def crear_reserva(event, context):
    # Nombre de la suscripción a la que te quieres suscribir
    subscription_path = 'projects/groovy-rope-416616/subscriptions/crear-reserva'

    # Suscribirse al tema
    future = subscriber.subscribe(subscription_path, callback=crear_reserva_callback)
    print(f"Suscripto a la suscripción {subscription_path}")

    # Mantener la función en ejecución
    future.result()