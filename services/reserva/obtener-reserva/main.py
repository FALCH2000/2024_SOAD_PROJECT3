import sqlalchemy
from google.cloud.sql.connector import Connector
import json
import datetime
import pytz


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


def obtener_todas_reservas():
    query = "SELECT * FROM Reservations;"
    result = usar_bd(query)
    mensaje = {}
    mensaje["data"] = []
    for elem in result:
        mensaje["data"].append({
            "Reservation_ID": elem[0],
            "User_ID": elem[1],
            "Number_Of_People": elem[2],
            "Date_Reserved": elem[3].strftime('%Y-%m-%d'),  # Convertir a cadena de texto en formato 'YYYY-MM-DD'
            "Start_Time": elem[4].strftime('%H:%M:%S'),    # Convertir a cadena de texto en formato 'HH:MM:SS'
            "End_Time": elem[5].strftime('%H:%M:%S')       # Convertir a cadena de texto en formato 'HH:MM:SS'
        })

    result_json = json.dumps(mensaje)
    return result_json

def obtener_reservas_pasadas(fecha,hora):
    # La query debe usar fecha y hora para obtener las reservas pasadas
    query = f"SELECT * FROM Reservations WHERE Date_Reserved < '{fecha}' OR Date_Reserved = '{fecha}' AND Start_Time < '{hora}';"
    result = usar_bd(query)
    mensaje = {}
    mensaje["data"] = []
    for elem in result:
        mensaje["data"].append({
            "Reservation_ID": elem[0],
            "User_ID": elem[1],
            "Number_Of_People": elem[2],
            "Date_Reserved": elem[3].strftime('%Y-%m-%d'),  # Convertir a cadena de texto en formato 'YYYY-MM-DD'
            "Start_Time": elem[4].strftime('%H:%M:%S'),    # Convertir a cadena de texto en formato 'HH:MM:SS'
            "End_Time": elem[5].strftime('%H:%M:%S')       # Convertir a cadena de texto en formato 'HH:MM:SS'
        })

    result_json = json.dumps(mensaje)
    return result_json
    

def obtener_reservas_futuras(fecha,hora):
    query = f"SELECT * FROM Reservations WHERE Date_Reserved = '{fecha}' AND Start_Time > '{hora}' OR Date_Reserved > '{fecha}';"
    result = usar_bd(query)
    mensaje = {}
    mensaje["data"] = []
    for elem in result:
        mensaje["data"].append({
            "Reservation_ID": elem[0],
            "User_ID": elem[1],
            "Number_Of_People": elem[2],
            "Date_Reserved": elem[3].strftime('%Y-%m-%d'),  # Convertir a cadena de texto en formato 'YYYY-MM-DD'
            "Start_Time": elem[4].strftime('%H:%M:%S'),    # Convertir a cadena de texto en formato 'HH:MM:SS'
            "End_Time": elem[5].strftime('%H:%M:%S')       # Convertir a cadena de texto en formato 'HH:MM:SS'
        })

    result_json = json.dumps(mensaje)
    return result_json


def obtener_reservas(request):
    request_args = request.args
    path = request.path
    respuesta = {}

    # Definir la zona horaria US-Central
    us_central_tz = pytz.timezone('US/Central')

    # Obtener la hora actual en la zona horaria US-Central
    hora_actual_us_central = datetime.datetime.now(us_central_tz)

    # Convertir a la zona horaria de Arizona
    zona_horaria_arizona = pytz.timezone('US/Arizona')
    hora_actual_arizona = hora_actual_us_central.astimezone(zona_horaria_arizona)

    hora_actual = hora_actual_us_central.strftime('%H:%M:%S')
    fecha_actual = hora_actual_us_central.strftime('%Y-%m-%d')

    print("Hora actual en US-Central (Texas):", hora_actual_us_central)
    print("Hora actual en Arizona:", hora_actual_arizona)

    """respuesta["hora_actual_us_central"] = str(hora_actual_us_central)
    respuesta["hora_actual_arizona"] = str(hora_actual_arizona)

    return (json.dumps(respuesta), 200)"""

    validate = (request_args.get("time") != "" and request_args.get("time") is not None)

    if not validate:
        respuesta["message"] = "Error: Peticion incorrecta"
        return (json.dumps(respuesta), 400)

    
    if path == "/" and request.method == 'GET' and "time" in request_args:
        tiempo = request_args.get("time")
        
        validate2 = (request_args.get("user_id") != "" and request_args.get("user_id") is not None)

        if tiempo == "all":
            return (obtener_todas_reservas(),200)
        elif tiempo == "pasadas":
            return (obtener_reservas_pasadas(fecha_actual,hora_actual),200)
        elif tiempo == "futuras":
            return (obtener_reservas_futuras(fecha_actual,hora_actual),200)
        else:
            respuesta["message"] = "Error: Peticion incorrecta"
            return (json.dumps(respuesta), 400)
    else:
        respuesta["message"] = "Error: Método no válido."
        return (json.dumps(respuesta), 404)