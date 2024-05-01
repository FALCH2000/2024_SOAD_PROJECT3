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
        print(f"row = {row}")
        data.append(row)  # Append each row to the list
    conn.close()
    return data  # Return the captured data

# Configura el cliente de Pub/Sub
subscriber = pubsub_v1.SubscriberClient()

def obtener_recomendacion_callback(message):
    # Procesa el mensaje recibido
    recomendacion = message.data.decode('utf-8')

    # convertir el mensaje a un diccionario
    recomendacion = json.loads(recomendacion)

    mensaje = {}
    mensaje["data"] = {}

    print(f"Mensaje recibido: {recomendacion}, version 0.0.1")
    if recomendacion["data"]["method"] == "obtener-recomendacion":
        if recomendacion["data"]["dish2"]["ID"] == None or recomendacion["data"]["dish2"]["ID"] == 0:
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
                        R.Main_Dish_ID = {recomendacion["data"]["dish1"]["ID"]} OR R.Drink_ID = {recomendacion["data"]["dish1"]["ID"]} OR R.Dessert_ID = {recomendacion["data"]["dish1"]["ID"]};"
            result = usar_bd(query)
            if len(result) == 0:
                mensaje["data"] = "No hay recomendaciones disponibles"
            else:
                for elem in result:
                    mensaje["data"]["Main_Dish"] = elem[0]
                    mensaje["data"]["Drink"] = elem[1]
                    mensaje["data"]["Dessert"] = elem[2]
            mensaje["status"] = 200
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
                        (R.Main_Dish_ID = {recomendacion["data"]['dish1']['ID']} AND R.Drink_ID = {recomendacion["data"]['dish2']['ID']} AND R.Dessert_ID = {recomendacion["data"]['dish2']['ID']}) OR\
                        (R.Main_Dish_ID = {recomendacion["data"]['dish1']['ID']} AND R.Drink_ID = {recomendacion["data"]['dish2']['ID']} AND R.Dessert_ID = {recomendacion["data"]['dish2']['ID']});"
            result = usar_bd(query)
            if len(result) == 0:
                mensaje["data"] = "No hay recomendaciones disponibles"
            else:
                for elem in result:
                    mensaje["data"]["Main_Dish"] = elem[0]
                    mensaje["data"]["Drink"] = elem[1]
                    mensaje["data"]["Dessert"] = elem[2]
    else:
        mensaje["status"] = 400
        mensaje["data"] = "Petición incorrecta"
    
    # Convertir el mensaje a JSON
    mensaje_json = json.dumps(mensaje)
    
    # Publica el mensaje de confirmación en el mismo tema de Pub/Sub
    publisher = pubsub_v1.PublisherClient()
    topic_path = 'projects/groovy-rope-416616/topics/recomendacion'
    publisher.publish(topic_path, data=mensaje_json.encode(), type='obtener-recomendacion-resultado')
    
    # Marca el mensaje como confirmado
    message.ack()


# entry point de la cloud function
def obtener_recomendacion(event, context):
    # Nombre de la suscripción a la que te quieres suscribir
    subscription_path = 'projects/groovy-rope-416616/subscriptions/obtener-recomendacion'

    # Suscribirse al tema
    future = subscriber.subscribe(subscription_path, callback=obtener_recomendacion_callback)
    print(f"Suscripto a la suscripción {subscription_path}")

    # Mantener la función en ejecución
    future.result()