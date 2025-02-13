import yaml
import pyodbc

from pymongo import MongoClient
import pymysql

def load_config(yaml_file="../config/db-config.yaml"):
    with open(yaml_file, "r") as file:
        config = yaml.safe_load(file)
    return config

# def get_mysql_connection():
#     config = load_config()['mysql']
#     try:
#         connection = pymysql.connect(
#             host=config["host"],
#             user=config["user"],
#             password=config["password"],
#             database=config["database"],
#             cursorclass=pymysql.cursors.DictCursor  # Optional, to return results as dictionaries
#         )
#         return connection
#     except pymysql.MySQLError as e:
#         print(f"Error: {e}") 
 

def get_mssql_connection():
    config = load_config()['mssql']
    try:
        connection = pyodbc.connect(
            driver=config["driver"],  
            server =config["server"],  
            database=config["database"],
            uid=config["user"],       
            pwd=config["password"],
            TrustServerCertificate="Yes"
            # cursorfactory=pyodbc.Cursor  
        )
        return connection
    except pyodbc.Error as e:
        print(f"Error: {e}")
