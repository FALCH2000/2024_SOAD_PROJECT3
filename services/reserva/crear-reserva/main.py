import sqlalchemy
from google.cloud.sql.connector import Connector
import json
from google.cloud import pubsub_v1
import jwt
import requests

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

def publicar_mensaje(respuesta):
    print(f"Publicando mensaje: {respuesta}")

    mensaje_json = json.dumps(respuesta)

    # Publica el mensaje de confirmación en el mismo tema de Pub/Sub
    publisher = pubsub_v1.PublisherClient()
    topic_path = 'projects/soa-project3/topics/reserva'
    publisher.publish(topic_path, data=mensaje_json.encode(), type='crear-reserva-resultado')


secret_key="6af00dfe63f6495195a3341ef6406c2c"
def crear_reserva_callback(message):
    # Procesa el mensaje recibido
    reserva = message.data.decode('utf-8')

    # convertir el mensaje a un diccionario
    reserva = json.loads(reserva)
    message.ack()

    # CAMBIAR EL FINAL DE LA URL
    url = f"https://us-central1-soa-project3.cloudfunctions.net/verificar-usuario/?token={reserva['token']}"

    response = requests.get(url)
    if response.status_code == 200:
        print("Codigo: 200. Token valido")
        print(response.json())
        print(f"Token: {reserva['token']}")
        token_decoded  = jwt.decode(jwt=reserva['token'], key=secret_key, algorithms=["HS256"])
    else:
        print("Codigo: 400. Token invalido")
        
        mensaje = {
            "data": "",
            "status": 400,
            "message": "Token invalido"
        }
        publicar_mensaje(mensaje)

        return

    # revisar que reserva tenga los atributos correctos, la cantidad de atributos y que no estén vacíos
    if not all(key in reserva['data'] for key in ['method', 'number_of_people', 'reservation_date', 'start_time', 'selected_tables']):
        print("Codigo: 400. Faltan atributos en la solicitud")
        mensaje = {
            "data": "",
            "status": 400,
            "message": "Faltan atributos en la solicitud"
        }
        publicar_mensaje(mensaje)
        return

    elif reserva['data']['method'] == "crear-reserva":
        try: 
            # TODO: verificar que haya disponibilidad de las mesas en la fecha y hora solicitada
            # for
            # verificar datos del usuario
            username = token_decoded['username']

            # verificar que la cantidad de personas de la reserva sea menor o igual a la capacidad de las mesas seleccionadas
            total_chairs = []
            for table in reserva['data']['selected_tables']:
                
                sillas = usar_bd(f"SELECT Chairs FROM Tables WHERE Table_Number = {table}")
              
                total_chairs.append(int(sillas[0][0]))
            
            print(f"TOTAL SILLAS: {sum(total_chairs)} y PERSONAS: {int(reserva['data']['number_of_people'])}")
            if sum(total_chairs) < int(reserva['data']['number_of_people']):
                print("Codigo: 400. Reserva no creada, eligio mal las mesas ya que le faltarian sillas.")
                
                mensaje = {
                    "data": "",
                    "status": 400,
                    "message": "Reserva no creada, eligio mal las mesas ya que le faltarian sillas."
                }
                publicar_mensaje(mensaje)

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
                
                mensaje = {
                    "data": "",
                    "status": 400,
                    "message": "Las horas de la potencial reserva no estan dentro del horario de atencion del restaurante"
                }
                publicar_mensaje(mensaje)
            
            reserva['data']['username'] = username

            insert_into_db(f"INSERT INTO Reservations (User_ID, Number_Of_People, Date_Reserved, Start_Time, End_Time)\
                    VALUES ('{reserva['data']['username']}', \
                            {reserva['data']['number_of_people']}, \
                            '{reserva['data']['reservation_date']}', \
                            '{reserva['data']['start_time']}', \
                            '{end_reservation_time}')")
            
            reservation_id = usar_bd(f"SELECT Reservation_ID FROM Reservations \
                                    WHERE User_ID = '{reserva['data']['username']}' \
                                    AND Date_Reserved = '{reserva['data']['reservation_date']}' \
                                    AND Start_Time = '{reserva['data']['start_time']}' \
                                    AND End_Time = '{end_reservation_time}'")
                    
            for table in reserva['data']['selected_tables']:
                
                insert_into_db(f"INSERT INTO Table_Availability (Table_ID, Date_Reserved, Start_Time, End_Time) \
                                VALUES ({table}, \
                                        '{reserva['data']['reservation_date']}', \
                                        '{reserva['data']['start_time']}', \
                                        '{end_reservation_time}')")
                
                insert_into_db(f"INSERT INTO Reservation_Tables_Association (Reservation_ID, Table_ID) \
                                VALUES ({str(reservation_id[0][0])}, \
                                        {table})")

            print("Codigo: 200, Reserva creada con éxito")
            mensaje = {
                "data": "",
                "status": 200,
                "message": "Reserva creada con éxito"
            }
            publicar_mensaje(mensaje)
            return
            
        except Exception as e:
            print(f"Codigo: 500. Error al crear la reserva: {str(e)}")
            mensaje = {
                "data": "",
                "status": 500,
                "message": f"Error al crear reserva: {str(e)}"
            } 
            publicar_mensaje(mensaje)
            return
            
    else:
        print("Codigo: 400. Metodo no soportado")
        mensaje = {
            "data": "",
            "status": 400,
            "message": "Bad Request. Metodo no valido"
        }


# entry point de la cloud function
def crear_reserva(event, context):
    # Nombre de la suscripción a la que te quieres suscribir
    subscription_path = 'projects/soa-project3/subscriptions/crear-reserva'

    # Suscribirse al tema
    future = subscriber.subscribe(subscription_path, callback=crear_reserva_callback)
    print(f"Suscripto a la suscripción {subscription_path}")

    # Mantener la función en ejecución
    future.result()