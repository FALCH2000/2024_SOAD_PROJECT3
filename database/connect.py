# Description: This file is used to connect to the SQL SERVER database in 
# a Google Cloud SQL SERVER instance. Just call the function connect_to_db()
# to get a connection to the database. The function test() is used to test the
# connection to the database.

import sqlalchemy
from google.cloud.sql.connector import Connector

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

# General function to connect to database
def connect_to_db():
    return get_engine().connect()

# Test function to test connection to database
def test():
    conn = connect_to_db()
    result = conn.execute("SELECT * FROM Food_Type")
    for row in result:
        print(row)
    conn.close()

test()
