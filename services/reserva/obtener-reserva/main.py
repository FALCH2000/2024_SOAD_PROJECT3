import sqlalchemy
from google.cloud.sql.connector import Connector
import json
import datetime
import pytz
import jwt
import requests


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


def obtener_todas_reservas(fecha, hora):
    print("Fecha: ", fecha)

    #query = "SELECT * FROM Reservations;"
    query = f"SELECT * FROM Reservations WHERE Date_Reserved = '{fecha}' AND Start_Time > '{hora}' OR Date_Reserved > '{fecha}';"
    result = usar_bd(query)
    print("RESULT: ", result)
    mensaje = {}
    mensaje["data"] = []

    if len(result) == 0:
        mensaje["data"] = "No hay reservas futuras"
        return json.dumps(mensaje)
    
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

def obtener_reservas_pasadas(fecha,hora, username):
    respuesta = {}
    
    # La query debe usar fecha y hora para obtener las reservas pasadas
    query = f"SELECT * FROM Reservations WHERE Date_Reserved < '{fecha}' OR Date_Reserved = '{fecha}' AND Start_Time < '{hora}' AND User_ID = '{username}';"
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
    

def obtener_reservas_futuras(fecha,hora, username):
    respuesta = {}
    
    query = f"SELECT * FROM Reservations WHERE Date_Reserved = '{fecha}' AND Start_Time > '{hora}' OR Date_Reserved > '{fecha}' AND User_ID = '{username}';"
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

def obtener_reserva_puntual(reservation_id):
    respuesta = {}
    
    query = f"SELECT * FROM Reservations WHERE Reservation_ID = '{reservation_id}';"
    result = usar_bd(query)
    mensaje = {}
    mensaje["data"] = []
    for elem in result:
        mensaje["data"].append({
            "Reservation_ID": elem[0],
            "Username": elem[1],
            "Number_Of_People": elem[2],
            "Date_Reserved": elem[3].strftime('%Y-%m-%d'),  # Convertir a cadena de texto en formato 'YYYY-MM-DD'
            "Start_Time": elem[4].strftime('%H:%M:%S'),    # Convertir a cadena de texto en formato 'HH:MM:SS'
            "End_Time": elem[5].strftime('%H:%M:%S')       # Convertir a cadena de texto en formato 'HH:MM:SS'
        })
    
    mensaje["status"] = 200
    mensaje["message"] = "Reserva encontrada"

    result_json = json.dumps(mensaje)
    return result_json


secret_key="6af00dfe63f6495195a3341ef6406c2c"
def obtener_reservas(request):
    try:
        print("REQUEST: ", request)
        
        # CORS related
        if request.method == "OPTIONS":
            # Allows GET requests from any origin with the Content-Type
            # header and caches preflight response for an 3600s
            headers = {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Max-Age": "3600",
            }

            return ("", 204, headers)
    
        headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
        }

        request_args = request.args
        print("REQUEST ARGS: ", request_args)
        path = request.path
        respuesta = {}

        print("BREAKPOINT 1")
        token_decoded = {}

        if "time" in request_args and request_args['time'] != "" and request_args['time'] is not None and request_args['time'] != "all":
            print("BREAKPOINT 2")

            # CAMBIAR EL FINAL DE LA URL
            url = f"https://us-central1-soa-project3.cloudfunctions.net/verificar-usuario/?token={request_args['token']}"

            response = requests.get(url)
            if response.status_code == 200:
                print("Codigo: 200. Token valido")
                print(response.json())
                print(f"Token: {request_args['token']}")
                token_decoded  = jwt.decode(jwt=request_args['token'], key=secret_key, algorithms=["HS256"])
            else:
                print("Codigo: 400. Token invalido")
                
                mensaje = {
                    "data": "",
                    "status": 400,
                    "message": "Token invalido"
                }
            
            username = token_decoded['username']

        print("BREAKPOINT 3")

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

        if "time" in request_args:
            validate = (request_args['time'] == "pasadas" or request_args['time'] == "futuras" or request_args['time'] == "all")
        else:
            validate = ("reservation_id" in request_args and request_args['reservation_id'] != "")
        if not validate:
            respuesta["message"] = "Error: Peticion incorrecta"
            return (json.dumps(respuesta), 400, headers)


        print("BREAKPOINT 4")

        if path == "/" and request.method == 'GET':
            if "time" in request_args:
                tiempo = request_args.get("time")
            
                if tiempo == "all":
                    return (obtener_todas_reservas(fecha_actual,hora_actual), 200, headers)
                elif tiempo == "pasadas":
                    return (obtener_reservas_pasadas(fecha_actual,hora_actual, username),200, headers)
                elif tiempo == "futuras":
                    return (obtener_reservas_futuras(fecha_actual,hora_actual, username),200, headers)
            
            elif "reservation_id" in request_args and request_args["reservation_id"] != "":
                return (obtener_reserva_puntual(request_args["reservation_id"]),200, headers)
            else:
                respuesta["message"] = "Error: Peticion incorrecta"
                return (json.dumps(respuesta), 400, headers)
        else:
            respuesta["message"] = "Error: Metodo no valido."
            return (json.dumps(respuesta), 404, headers)
    except Exception as e:
        respuesta["message"] = f"Error: {e}"
        return (json.dumps(respuesta), 404, headers)