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

def obtener_calendario_callback(date_request, start_time_request):
    # json de respuesta
    mensaje = {}
    mensaje['available_tables'] = []

    # Obtener todas las mesas disponibles para una fecha y hora especifica

    try:
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

        print("End time print: " + end_time)
        print(" ")

        mesas_ocupadas = usar_bd(f"SELECT * FROM Table_Availability WHERE Date_Reserved = '{date_request}' AND Start_Time >= '{start_time_request}' AND End_Time <= '{end_time}'")
        
        # cuando no hay mesas ocupadas
        if len(mesas_ocupadas) == 0:
            for mesa in mesas:
                mensaje['available_tables'].append({"Table_ID": mesa[0], "Chairs" : mesa[1]})
        else:
            print("Hay mesas ocupadas")
            # cuando si hay mesas ocupadas
            for mesa in mesas:
                busy_table = True
                for mesa_ocupada in mesas_ocupadas:
                    if mesa[0] == mesa_ocupada[0]:
                        busy_table = False
                        break

                if busy_table:
                    mensaje['available_tables'].append({"Table_ID": mesa[0], "Chairs" : mesa[1]})

 
        mensaje['status'] = 200
        mensaje['message'] = "Calendario obtenido correctamente"

    except Exception as e:
        mensaje['status'] = 500
        mensaje['message'] = f"Error al obtener el calendario: {str(e)}"

    # Convertir el mensaje a JSON
    mensaje_json = json.dumps(mensaje)

    return (mensaje_json, mensaje['status'])

# entry point de la cloud function
def obtener_calendario(request):
    print("Obtener calendario")
    request_args = request.args
    path = request.path
    respuesta = {}

    print("Antes de validar")
    validate = (request_args.get('date') != "" and request_args.get('start_time') != "")

    respuesta = {}
    print("AAAAAAAAAAAAAAAAAAAA")
    print(" ")
    if validate:
        print("Validación exitosa")
        return obtener_calendario_callback(request_args.get('date'), request_args.get('start_time'))
    else:
        respuesta["status"] = 404
        respuesta["message"] = "Error: Método no válido."
        return f"{json.dumps(respuesta, ensure_ascii=False)}"