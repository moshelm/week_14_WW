import mysql.connector
from mysql.connector import errorcode
from .models import SetData,DataF
import os 


DATABASE_USER = os.getenv('DATABASE_USER','root')
DATABASE_NAME = os.getenv('DATABASE_NAME','weapon_db')
DATABASE_PORT = int(os.getenv('DATABASE_PORT','3306'))
DATABASE_HOST = os.getenv('DATABASE_HOST','127.0.0.1')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD','')
TABLE_NAME = os.getenv('TABLE_NAME','weapon_table')


DATABASE_CONFIG = {
    'host':DATABASE_HOST,
    'port':DATABASE_PORT,
    'password':DATABASE_PASSWORD,
    'user':DATABASE_USER}

def connect_to_mysql(use_db=True):
    config = DATABASE_CONFIG.copy()
    if use_db:
        config['database'] = DATABASE_NAME
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except mysql.connector.Error as err:
        print(f'connection failed {err}')
        return None


def get_db_coonection():
    try:
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        yield conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('error usr or password wrong')
        elif err.errno ==errorcode.ER_BAD_DB_ERROR:
            print('database not exists')
        else:
            print(f'db error {err}')
    finally:
        if conn and conn.is_connected():
            conn.close()

def init_database():
    conn = connect_to_mysql(use_db=False)
    if not conn:
        return False
    try:
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
        print("Database creation: SUCCESS")
        return True
    except mysql.connector.Error as err:
        print(f"Database creation FAILED: {err}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def init_table():
    conn = connect_to_mysql(use_db=True)
    if not conn:
        return False
    
    statement = f"""CREATE TABLE IF NOT EXISTS {TABLE_NAME}(
                id INT AUTO_INCREMENT PRIMARY KEY,
                weapon_id VARCHAR(100),
                weapon_name VARCHAR(100),
                weapon_type VARCHAR(100), 
                range_km INT,
                weight_kg DECIMAL,
                manufacturer VARCHAR(100), 
                origin_country VARCHAR(100), 
                storage_location VARCHAR(100), 
                year_estimated INT,
                risk_level VARCHAR(100))
                """ 
    try:
        cursor = conn.cursor()
        cursor.execute(f'USE {DATABASE_NAME}')
        cursor.execute(statement)
        return True
    except mysql.connector.Error as err:
        print(f'table creatation failed {err}')
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

def insert_db(data:DataF):
    conn = connect_to_mysql(use_db=True)
    if not conn:
        return "failed: no connection"
    fields : list = list(data.records[0].model_dump().keys())
    values = [tuple(record.model_dump().values()) for record in data.records]
    columns = ','.join(fields)
    
    flags = ','.join(['%s'] * len(fields))
    statement = f'INSERT INTO {TABLE_NAME} ({columns}) VALUES ({flags})'
    try:
        cursor = conn.cursor()
        cursor.execute(f'USE {DATABASE_NAME}')
        cursor.executemany(statement,values)
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print(f'insert failed {err}')
        return False
    finally:
       if conn.is_connected():
            cursor.close()
            conn.close()
