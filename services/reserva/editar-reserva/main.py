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

def usar_bd_sin_return(solicitud):
    conn = get_engine().connect()
    conn.execute(solicitud)
    conn.close()

def sumar_hora(start_time_request):
    decena = start_time_request[0]
    unidad = start_time_request[1]
    end_time = ""
    # sumar 2 horas a la hora de inicio para obtener la hora de fin
    if decena == "0":  
        suma = int(unidad) + 2

        if suma < 10:
            end_time = "0" + str(suma) + start_time_request[2:]
        else:
            end_time = str(suma) + start_time_request[2:]

    elif decena == "1":
        suma = int(decena)*10 + int(unidad) + 2
        end_time = str(suma) + start_time_request[2:]
    
    elif decena == "2":
        suma = int(decena)*20 + int(unidad) + 2

        if suma < 25:
            end_time = str(suma) + start_time_request[2:]
        else: # si la suma es mayor a 24
            end_time = "00" + start_time_request[2:]
    
    return end_time

# Funcion que compara dos horas en formato "HH:MM:SS"
def hora1_menor_hora2(hora1, hora2):
    if hora1 < hora2:
        return True
    else:
        return False


secret_key="6af00dfe63f6495195a3341ef6406c2c"
def editar_reserva_callback(message):
    # las validaciones y el codigo es muy parecido a la funcion de crear reserva
    # por lo que se reutiliza el codigo
    # Procesa el mensaje recibido
    reserva = message.data.decode('utf-8')

    # convertir el mensaje a un diccionario
    reserva = json.loads(reserva)
    message.ack()

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
    exp_date = token_decoded['exp']
    print(f"Username: {username} y exp_date: {exp_date}")
    
    # validar que el mensaje tenga los campos necesarios
    if not all(key in reserva['data'] for key in ['method', 'reservation_id', 'number_of_people', 'reservation_date', 'start_time', 'selected_tables']):
        print("Codigo: 400. Faltan atributos en la solicitud editar-reserva")

    elif reserva['data']['method'] == "editar-reserva":
        try:

            # TODO: verificar que haya disponibilidad de las mesas en la fecha y hora solicitada
            # for
            
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

            # verificar que la reserva exista
            reserva_verification = usar_bd(f"SELECT * FROM Reservations WHERE Reservation_ID = {reserva['data']['reservation_id']}")
            old_data = reserva_verification[0]
            if reserva_verification == []:
                print("Codigo: 404. La reserva no existe")
                return

            # Suponiendo que reserva_verification contiene cadenas para fecha y hora
            old_date = reserva_verification[0][3].strftime('%Y-%m-%d')
            old_start_time = reserva_verification[0][4].strftime('%H:%M:%S')
            print(f"old date = {old_date} old start time = {old_start_time}")

            # verificar si la reserva es futura
            if fecha_actual > reserva['data']['reservation_date']:
                print("Codigo: 400. No se puede editar una reserva pasada")
                #mensaje['status'] = '400'
                #mensaje['message'] = 'No se puede eliminar una reserva pasada'
                return #json.dumps(mensaje)
            
            total_chairs = []
            for table in reserva['data']['selected_tables']:
                
                sillas = usar_bd(f"SELECT Chairs FROM Tables WHERE Table_Number = {table}")
                print(f"SILLAS: {sillas[0][0]}")
                total_chairs.append(int(sillas[0][0]))
            
            # verificar que la cantidad de personas de la reserva sea menor o igual a la capacidad de las mesas seleccionadas
            print(f"TOTAL SILLAS: {sum(total_chairs)} y PERSONAS: {int(reserva['data']['number_of_people'])}")
            if sum(total_chairs) < int(reserva['data']['number_of_people']):
                print("Codigo: 400. Reserva no creada, eligio mal las mesas ya que le faltarian sillas.")
                return
            
            # verificar que las horas de la reserva esten dentro del horario de atencion del restaurante
            hora_apertura_restaurante = usar_bd(f"SELECT Opening_Time FROM Restaurant_Data WHERE Local_ID = 1")
            print(f"HORA DE APERTURA: {str(hora_apertura_restaurante[0][0])}")
            hora_cierre_restaurante = usar_bd(f"SELECT Closing_Time FROM Restaurant_Data WHERE Local_ID = 1")
            end_reservation_time = sumar_hora(reserva['data']['start_time'])
            after_aperture_time = hora1_menor_hora2(str(hora_apertura_restaurante[0][0]), reserva['data']['start_time'])
            before_closing_time = hora1_menor_hora2(end_reservation_time, str(hora_cierre_restaurante[0][0]))

            if after_aperture_time == False or before_closing_time == False:
                print("Codigo: 400. Las horas de la potencial reserva no estan dentro del horario de atencion del restaurante")
                return
            
            usar_bd_sin_return(f"UPDATE Reservations SET \
                    Number_Of_People = {reserva['data']['number_of_people']}, \
                    Date_Reserved = '{reserva['data']['reservation_date']}', \
                    Start_Time = '{reserva['data']['start_time']}', \
                    End_Time = '{end_reservation_time}' \
                    WHERE Reservation_ID = {reserva['data']['reservation_id']} AND User_ID = '{reserva['data']['username']}'")

            print("Reserva actualizada")

            for table in reserva['data']['selected_tables']:
                # actualizar la tabla de disponibilidad de mesas
                usar_bd_sin_return(f"DELETE FROM Table_Availability \
                        WHERE Table_ID = {table} \
                        AND Date_Reserved = '{old_date}' \
                        AND Start_Time = '{old_start_time}' \
                        AND End_Time = '{sumar_hora(old_start_time)}'")
                
                usar_bd_sin_return(f"INSERT INTO Table_Availability (Table_ID, Date_Reserved, Start_Time, End_Time) \
                        VALUES ({table}, '{reserva['data']['reservation_date']}', '{reserva['data']['start_time']}', '{end_reservation_time}')")
                
                # actualizar la tabla de asociacion de mesas con reservas
                usar_bd_sin_return(f"DELETE FROM Reservation_Tables_Association \
                                   WHERE Reservation_ID = {reserva['data']['reservation_id']} \
                                   AND Table_ID = {table}")
                
                usar_bd_sin_return(f"INSERT INTO Reservation_Tables_Association (Reservation_ID, Table_ID) \
                                   VALUES ({reserva['data']['reservation_id']}, {table})")

            print("Mesas actualizadas")
        except Exception as e:
            print(f"Codigo: 500. Error: {e}")

# entry point de la cloud function
def editar_reserva(event, context):
    # Nombre de la suscripción a la que te quieres suscribir
    subscription_path = 'projects/soa-project3/subscriptions/editar-reserva'

    # Suscribirse al tema
    future = subscriber.subscribe(subscription_path, callback=editar_reserva_callback)
    print(f"Suscripto a la suscripción {subscription_path}")

    # Mantener la función en ejecución
    future.result()