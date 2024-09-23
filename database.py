# database.py
import psycopg2
from psycopg2 import pool

# Pool de conexiones para manejar múltiples solicitudes
connection_pool = pool.SimpleConnectionPool(
    1, 20,
    host="localhost",
    database="energia_db",
    user="postgres",
    password="12345678"
)

def get_db_connection():
    try:
        connection = connection_pool.getconn()
        return connection
    except Exception as error:
        print(f"Error al obtener conexión: {error}")
        return None

def release_db_connection(connection):
    connection_pool.putconn(connection)
