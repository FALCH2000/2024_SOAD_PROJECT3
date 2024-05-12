import sqlalchemy
from google.cloud.sql.connector import Connector
import json
from google.cloud import pubsub_v1
import datetime
import pytz
import jwt

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

def delete_from_db(solicitud):
    conn = get_engine().connect()
    conn.execute(solicitud)
    conn.close()

secret_key="6af00dfe63f6495195a3341ef6406c2c"
def eliminar_reserva_callback(message):
    # Procesa el mensaje recibido
    reservaporborrar = message.data.decode('utf-8')

    # convertir el mensaje a un diccionario
    reservaporborrar = json.loads(reservaporborrar)
    # Marca el mensaje como confirmado
    message.ack()

    # json de respuesta
    mensaje = {}

    respuesta = {}
    #verificar el token
    try:
        token_decoded  = jwt.decode(jwt=message.args.get('token'), key=secret_key)
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

    if  not all(key in reservaporborrar['data'] for key in ['method', 'reservation_id', 'reservation_date', 'start_time']):
        print("Faltan datos en la solicitud")
        mensaje['status'] = '400'
        mensaje['message'] = 'Faltan datos en la solicitud'
        return mensaje
    
    elif reservaporborrar['data']['method'] == "eliminar-reserva":
        try:
            print(f"reservaporborrar = {reservaporborrar['data']['reservation_id']}")
            print(f"fecha_actual {fecha_actual} vs date_reservada {reservaporborrar['data']['reservation_date']}")

            # verificar si la reserva es futura
            if fecha_actual > reservaporborrar['data']['reservation_date']:
                print("No se puede eliminar una reserva pasada")
                mensaje['status'] = '400'
                mensaje['message'] = 'No se puede eliminar una reserva pasada'
                return json.dumps(mensaje)
            
            # verificar que la reserva exista
            reserva_verification = usar_bd(f"SELECT * FROM Reservations WHERE Reservation_ID = {reservaporborrar['data']['reservation_id']}")
            if reserva_verification == []:
                print("La reserva no existe")
                mensaje['status'] = '404'
                mensaje['message'] = 'La reserva no existe'
                return json.dumps(mensaje)
            print(f"reservaporborrar = {reserva_verification[0][0]}")

            # obtener las mesas asociadas a la reserva
            mesasporliberar = usar_bd(f"SELECT Table_ID FROM Reservation_Tables_Association WHERE Reservation_ID = {reservaporborrar['data']['reservation_id']}")
            print(f"mesasporliberar = {mesasporliberar}")
            print(f"mesasporliberar = {mesasporliberar[0][0]}")  # [#row][#column]
            
            # verificar si la reserva tiene mesas asociadas
            if mesasporliberar == []:
                print("La reserva no tiene mesas asociadas")
                mensaje['status'] = '404'
                mensaje['message'] = 'La reserva no tiene mesas asociadas'
                return json.dumps(mensaje)

            delete_from_db(f"DELETE FROM Reservation_Tables_Association WHERE Reservation_ID = {reservaporborrar['data']['reservation_id']}")
            print("Mesas desasociadas de la reserva")

            # liberar las mesas ocupadas
            for row in mesasporliberar:
                delete_from_db(f"DELETE FROM Table_Availability WHERE Table_ID = {str(row[0])} \
                            AND Date_Reserved = '{reservaporborrar['data']['reservation_date']}' \
                            AND Start_Time = '{reservaporborrar['data']['start_time']}'")
                
            print("Mesas liberadas")

            delete_from_db(f"DELETE FROM Reservations WHERE Reservation_ID = {reservaporborrar['data']['reservation_id']}")
            print("Reserva eliminada")

            mensaje['status'] = '200'
            mensaje['message'] = 'Reserva eliminada'

        except Exception as e:
            mensaje['status'] = '500'
            mensaje['message'] = f'Error al eliminar la reserva: {str(e)}'

    # Convertir el mensaje a JSON
    mensaje_json = json.dumps(mensaje)
    
    # Publica el mensaje de confirmación en el mismo tema de Pub/Sub
    publisher = pubsub_v1.PublisherClient()
    topic_path = 'projects/soa-project3/topics/reserva'
    publisher.publish(topic_path, data=mensaje_json.encode(), type='eliminar-reserva-resultado')

def eliminar_reserva(event, context):
    # Nombre de la suscripción a la que te quieres suscribir
    subscription_path = 'projects/soa-project3/subscriptions/eliminar-reserva'

    # Suscribirse al tema
    future = subscriber.subscribe(subscription_path, callback=eliminar_reserva_callback)
    print(f"Suscripto a la suscripción {subscription_path}")

    # Mantener la función en ejecución
    future.result()