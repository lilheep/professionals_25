from peewee import MySQLDatabase
from pymysql import MySQLError
import pymysql

DB_NAME = 'xzxzxz'
DB_USER = 'root'
DB_PASSWORD = 'root'
DB_HOST = '127.0.0.1'
DB_PORT = 3306

def init_database():
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )
        with connection.cursor() as cursor:
                cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME}')
                print('Database instalizade!')
    except MySQLError as e:
        print(f'Database not instalizatade: {e}')
    
    finally:
        if 'connection' in locals() and connection:
            connection.close()

init_database()

db_connection = MySQLDatabase(
    DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
            
    