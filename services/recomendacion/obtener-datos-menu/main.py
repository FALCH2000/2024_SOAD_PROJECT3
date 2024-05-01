"""
Devuelve las comidas por cada tipo
SELECT * FROM Food
INNER JOIN Food_Type_Association
ON Food.ID = Food_Type_Association.Food_ID
WHERE Food_Type_Association.Type_ID = 1;

Devuelve los tipos de comida
SELECT * FROM Food_Type;
"""

# Description: This file is used to connect to the SQL SERVER database in 
# a Google Cloud SQL SERVER instance. Just call the function connect_to_db()
# to get a connection to the database. The function test() is used to test the
# connection to the database.

import sqlalchemy
from google.cloud.sql.connector import Connector
import json
from google.cloud import pubsub_v1

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
        data.append(row)  # Append each row to the list
    conn.close()
    return data  # Return the captured data

# Configura el cliente de Pub/Sub
subscriber = pubsub_v1.SubscriberClient()

def obtener_menu_callback(message):
    # Procesa el mensaje recibido
    request = message.data.decode('utf-8')
    # convertir el mensaje a un diccionario
    request = json.loads(request)
    mensaje = {}
    mensaje["data"] = {}
    mensaje["data"]["types"] = []
    mensaje["data"]["MainCourses"] = []
    mensaje["data"]["Drinks"] = []
    mensaje["data"]["Desserts"] = []

    if request["data"] == "obtener-menu":
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

    else:
        mensaje["status"] = 400
        mensaje["message"] = "Petición incorrecta"
    
    # Convertir el mensaje a JSON
    mensaje_json = json.dumps(mensaje)

    # Publica el mensaje de confirmación en el mismo tema de Pub/Sub
    publisher = pubsub_v1.PublisherClient()
    topic_path = 'projects/groovy-rope-416616/topics/recomendacion'
    publisher.publish(topic_path, data=mensaje_json.encode(), type='obtener-menu-resultado')
    
    # Marca el mensaje como confirmado
    message.ack()

# entry point de la cloud function
def obtener_menu(event, context):
    # Nombre de la suscripción a la que te quieres suscribir
    subscription_path = 'projects/groovy-rope-416616/subscriptions/obtener-menu'

    # Suscribirse al tema
    future = subscriber.subscribe(subscription_path, callback=obtener_menu_callback)
    print(f"Suscripto a la suscripción {subscription_path}")

    # Mantener la función en ejecución
    future.result()
