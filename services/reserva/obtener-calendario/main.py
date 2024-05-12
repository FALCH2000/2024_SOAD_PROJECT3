import sqlalchemy
from google.cloud.sql.connector import Connector
import json

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

def obtener_calendario_callback(date_request, start_time_request, headers):
    # json de respuesta
    mensaje = {}
    mensaje['data'] = {}
    mensaje['data']['available_tables'] = []

    # Obtener todas las mesas disponibles para una fecha y hora especifica

    try:
        print("Date request: " + date_request)
        print("Start time request: " + start_time_request)

        # obtener todas las mesas
        mesas = usar_bd("SELECT * FROM Tables")

        # obtener las mesas ocupadas para esa fecha y hora
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

        print("End time  " + end_time)

        mesas_ocupadas = usar_bd(f"SELECT * FROM Table_Availability WHERE Date_Reserved = '{date_request}' AND Start_Time >= '{start_time_request}' AND End_Time <= '{end_time}'")
        
        # cuando todas las mesas estan ocupadas, no hay mesas disponibles
        # esto puede pasar en eventos especiales
        if len(mesas_ocupadas) == len(mesas):
            print("No hay mesas disponibles para la fecha y hora solicitada.")
            mensaje['data']['available_tables'] = []
            mensaje['status'] = 404
            mensaje['message'] = "No hay mesas disponibles para la fecha y hora solicitada."
            return (json.dumps(mensaje), mensaje['status'], headers)

        # cuando no hay mesas ocupadas
        if len(mesas_ocupadas) == 0:
            print("Todas las mesas estan disponibles para la fecha y hora solicitada")
            for mesa in mesas:
                print("Dentro del for")
                print("MESA: ", mesa)
                mensaje['data']['available_tables'].append({"Table_ID": mesa[0], "Chairs" : mesa[1]})
        else:
            print("Hay algunas mesas ocupadas para la fecha y hora solicitada")
            # cuando si hay mesas ocupadas
            for mesa in mesas:
                busy_table = True
                for mesa_ocupada in mesas_ocupadas:
                    if mesa[0] == mesa_ocupada[0]:
                        busy_table = False
                        break

                if busy_table:
                    mensaje['data']['available_tables'].append({"Table_ID": mesa[0], "Chairs" : mesa[1]})

 
        mensaje['status'] = 200
        mensaje['message'] = "Mesas disponibles obtenidas correctamente."

    except Exception as e:
        mensaje['status'] = 500
        mensaje['message'] = f"Error al obtener el calendario: {str(e)}"

    # Convertir el mensaje a JSON
    mensaje_json = json.dumps(mensaje)

    return (mensaje_json, mensaje['status'], headers)

# entry point de la cloud function
def obtener_calendario(request):
    # Set CORS headers for the preflight request
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
    
    request_args = request.args
    path = request.path
    respuesta = {}
    validate = (request_args.get('date') != "" and request_args.get('start_time') != "")
    respuesta = {}
    
    # Set CORS headers for main requests
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
    }
    
    if path == "/" and request.method == 'GET' and validate:
        return obtener_calendario_callback(request_args.get('date'), request_args.get('start_time'), headers)
    
    else:
        respuesta['data']['available_tables'] = []
        respuesta["status"] = 404
        respuesta["message"] = "Error: Método no válido."
        return (f"{json.dumps(respuesta)}", respuesta["status"], headers)