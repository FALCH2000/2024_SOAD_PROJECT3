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


def obtener_recomendacion_callback(recomendacion, quantity):
    mensaje = {}
    mensaje["data"] = {}

    if quantity == 1:
        query = f"SELECT \
                    Main_Dish.Name AS Main_Dish,\
                    Drink.Name AS Drink,\
                    Dessert.Name AS Dessert\
                FROM \
                    Recommendation R\
                INNER JOIN \
                    Food Main_Dish ON R.Main_Dish_ID = Main_Dish.ID\
                INNER JOIN \
                    Food Drink ON R.Drink_ID = Drink.ID\
                INNER JOIN \
                    Food Dessert ON R.Dessert_ID = Dessert.ID\
                WHERE \
                    R.Main_Dish_ID = {recomendacion[0]} OR R.Drink_ID = {recomendacion[0]} OR R.Dessert_ID = {recomendacion[0]};"
        result = usar_bd(query)
        if len(result) == 0:
            mensaje["data"] = "No hay recomendaciones disponibles"
        else:
            for elem in result:
                mensaje["data"]["Main_Dish"] = elem[0]
                mensaje["data"]["Drink"] = elem[1]
                mensaje["data"]["Dessert"] = elem[2]
    else:
        query = f"SELECT \
                    Main_Dish.Name AS Main_Dish,\
                    Drink.Name AS Drink,\
                    Dessert.Name AS Dessert\
                FROM \
                    Recommendation R\
                INNER JOIN \
                    Food Main_Dish ON R.Main_Dish_ID = Main_Dish.ID\
                INNER JOIN \
                    Food Drink ON R.Drink_ID = Drink.ID\
                INNER JOIN \
                    Food Dessert ON R.Dessert_ID = Dessert.ID\
                WHERE \
                    (R.Main_Dish_ID = {recomendacion[0]} AND R.Drink_ID = {recomendacion[1]}) OR\
                    (R.Main_Dish_ID = {recomendacion[1]} AND R.Drink_ID = {recomendacion[0]}) OR\
                    (R.Main_Dish_ID = {recomendacion[0]} AND R.Dessert_ID = {recomendacion[1]}) OR\
                    (R.Main_Dish_ID = {recomendacion[1]} AND R.Dessert_ID = {recomendacion[0]}) OR\
                    (R.Drink_ID = {recomendacion[0]} AND R.Dessert_ID = {recomendacion[1]}) OR\
                    (R.Drink_ID = {recomendacion[1]} AND R.Dessert_ID = {recomendacion[0]});"

        result = usar_bd(query)
        # R.Dessert_ID = {recomendacion["data"]['dish2']['ID']}
        if len(result) == 0:
            mensaje["data"] = "No hay recomendaciones disponibles"
        else:
            for elem in result:
                mensaje["data"]["Main_Dish"] = elem[0]
                mensaje["data"]["Drink"] = elem[1]
                mensaje["data"]["Dessert"] = elem[2]
    
    # Convertir el mensaje a JSON
    mensaje_json = json.dumps(mensaje)
    
    return mensaje_json


def obtener_recomendacion(request):
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
    # Set CORS headers for main requests
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Credentials": "true",
    }
    validate = (request_args["dish1"] != 0 and request_args["dish1"] is not None and request_args.get("dish1") != "")

    if not validate:
        respuesta["message"] = "Error: Peticion incorrecta"
        return (json.dumps(respuesta), 400, headers)

    
    if path == "/" and request.method == 'GET' and "dish1" in request_args:
        dish1_id = request_args.get("dish1")
        
        if "dish2" not in request_args:
            dishes = (dish1_id)
            return (obtener_recomendacion_callback(dishes, 1), 200,headers)
        else:
            validate2 = (request_args["dish2"] != 0 and request_args["dish2"] is not None and request_args.get("dish2") != "")
            if not validate2:
                respuesta["message"] = "Error: Peticion incorrecta"
                return (json.dumps(respuesta), 400,headers)
            dish2_id = request_args.get("dish2")
            if dish2_id is None or dish2_id == "0":
                respuesta["message"] = "Error: Peticion incorrecta"
                return (json.dumps(respuesta), 400,headers)
            dishes = (dish1_id, dish2_id)
            return (obtener_recomendacion_callback(dishes, 2), 200,headers)
    else:
        respuesta["message"] = "Error: Método no válido."
        return (json.dumps(respuesta), 404,headers)
