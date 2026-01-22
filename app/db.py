import mysql.connector
from .models import SetData,DataF
import os 


DATABASE_USER = os.getenv('DATABASE_USER','root')
DATABASE_NAME = os.getenv('DATABASE_NAME','weapon_db')
DATABASE_PORT = int(os.getenv('DATABASE_PORT','3306'))
DATABASE_HOST = os.getenv('DATABASE_HOST','127.0.0.1')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD','')
TABLE_NAME = os.getenv('TABLE_NAME','weapon_table')

conn = mysql.connector.connect(host=DATABASE_HOST,port=DATABASE_PORT,user=DATABASE_USER,password=DATABASE_PASSWORD)


def init_database():
    try: 
        with conn.cursor() as cursor:
            statement = f'CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}'
            cursor.execute(statement)
            cursor.close()
    except mysql.connector.errors as error:
        print(f'database faild connect{error}')
    finally:
        cursor.close()


def init_table():
    try: 
        with conn.cursor() as cursor:
            cursor.execute(f'USE {DATABASE_NAME}')
            
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
            cursor.execute(statement)
    # except mysql.connector.errors as error:
    #     print(f'TABLE faild connect{error}')
    finally:
        cursor.close()
def insert_db(data:DataF):
    try: 
        with conn.cursor() as cursor:
            cursor.execute(f'USE {DATABASE_NAME}')
            fields : list = list(data.records[0].model_dump().keys())
            values = [tuple(record.model_dump().values()) for record in data.records]
            columns = ','.join(fields)
            
            flags = ','.join(['%s'] * len(fields))
            statement = f'INSERT INTO {TABLE_NAME} ({columns}) VALUES ({flags})'
            
            cursor.executemany(statement,values)
    except mysql.connector.errors as error:
        print(f'insert faild connect{error}')
    finally:
        conn.close()
