import sqlalchemy
from google.cloud.sql.connector import Connector
import json

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
        data.append(row)  # Append each row to the list
    conn.close()
    return data  # Return the captured data



def obtener_menu_callback(message):
    mensaje = {}
    mensaje["data"] = {}
    mensaje["data"]["types"] = []
    mensaje["data"]["MainCourses"] = []
    mensaje["data"]["Drinks"] = []
    mensaje["data"]["Desserts"] = []

    
    food_types = usar_bd("SELECT * FROM Food_Type;")

    for row in food_types:
        food_type_id = row[0]
        food_type_name = row[1]
        mensaje["data"]["types"].append({"id": food_type_id, "name": food_type_name})
    
    main_courses = usar_bd("SELECT ID, Name\
                FROM Food\
                WHERE ID IN (\
                SELECT Food_ID\
                FROM Food_Type_Association\
                WHERE Type_ID = (SELECT ID FROM Food_Type WHERE Name = 'MainCourse'));")
    for row in main_courses:
        main_course_id = row[0]
        main_course_name = row[1]
        mensaje["data"]["MainCourses"].append({"id": main_course_id, "name": main_course_name})

    drinks = usar_bd("SELECT ID, Name\
                FROM Food\
                WHERE ID IN (\
                SELECT Food_ID\
                FROM Food_Type_Association\
                WHERE Type_ID = (SELECT ID FROM Food_Type WHERE Name = 'Drink'));")
    for row in drinks:
        drink_id = row[0]
        drink_name = row[1]
        mensaje["data"]["Drinks"].append({"id": drink_id, "name": drink_name})

    desserts = usar_bd("SELECT ID, Name\
                FROM Food\
                WHERE ID IN (\
                SELECT Food_ID\
                FROM Food_Type_Association\
                WHERE Type_ID = (SELECT ID FROM Food_Type WHERE Name = 'Dessert'));")
    for row in desserts:
        dessert_id = row[0]
        dessert_name = row[1]
        mensaje["data"]["Desserts"].append({"id": dessert_id, "name": dessert_name})

    mensaje["status"] = 200
    mensaje["message"] = "Menu obtenido correctamente"
    
    # Convertir el mensaje a JSON
    mensaje_json = json.dumps(mensaje)

    return mensaje_json


# entry point de la cloud function
def obtener_menu(request):
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

    request_json = request.get_json(silent=True)
    request_args = request.args
    path = (request.path)
    respuesta = {}
    # Set CORS headers for main requests
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
    }
    if path == "/" and request.method == 'GET' and request_json is None and not request_args:
        return (obtener_menu_callback(request),200,headers)
    else:
        respuesta["status"] = 404
        respuesta["message"] = "Error: Método no válido."
        return (f"{json.dumps(respuesta, ensure_ascii=False)}",404,headers)
