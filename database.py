from peewee import MySQLDatabase
from pymysql import MySQLError
import pymysql

DB_HOST = 'localhost'
DB_PORT = 3306
DB_NAME = 'prof_database'
DB_USERNAME = 'root'
DB_PASSWORD = 'root'

def init_database():
    '''Creating database!'''
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD
        )
        
        with connection.cursor() as cursor:
            cursor.execute(f'CREATE DATABASE IF NOT EXISTS {DB_NAME};')
            
            print(f'Database {DB_NAME} is initialized!')
        
    except MySQLError as e:
        print(f'Error creating database: {e}')
    
    finally:
        if 'connection' in locals() and connection:
            connection.close()
            
init_database()

db_connection = MySQLDatabase(
    DB_NAME,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
    