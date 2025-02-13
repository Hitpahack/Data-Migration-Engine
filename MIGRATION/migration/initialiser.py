import sys
import time
import os
import yaml
import getpass
import pandas as pd
from tabulate import tabulate

import datetime
import pytz



sys.path.append('../')
from  utils import art
from mappers import mysql_connector

def load_config(yaml_file="../config/db-config.yaml"):
    with open(yaml_file, "r") as file:
        config = yaml.safe_load(file)
    return config



def printTitle():
    print("+---------------------------------------------------------------+")
    art.textArt("Migration tool")
    print("+---------------------------------------------------------------+")


def loading_spinner(seconds, message="Please wait", symbol="⠋"):
    for _ in range(int(seconds)):
        sys.stdout.write(f"\r\033[91m{message} \033[0m{symbol}")  
        sys.stdout.flush()
        time.sleep(0.1)
        symbol = symbol[-1] + symbol[:-1]  
    sys.stdout.write('\r\033[0m')  
    sys.stdout.flush()

def printAbility():
    print("Migrate any MySQL db to mongodb with or without retaining relations")

def get_db_input_and_create_config(config_folder="../config", config_file="db-config.yaml"):
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)

    config_path = os.path.join(config_folder, config_file)

    # #Get MYSQL connection details
    # configs = {}
    # configs['mysql'] = {}
    # print("\n--------------Enter SOURCE MYSQL DB connection details--------------")
    
    # #Host
    # print("Enter host:")
    # configs['mysql']['host'] = input()
    
    # #Port number
    # print("Enter port:")
    # configs['mysql']['port'] = int(input())
    
    # #username
    # print("Enter username:")
    # configs['mysql']['user'] = input()
    
    # #Password
    # configs['mysql']['password'] = get_password()
    
    # #DB name
    # print("Enter db name:")
    # configs['mysql']['database'] = input()
    
    configs = {}
    configs["mssql"] = {}

    configs["mssql"]["driver"] = "ODBC Driver 18 for SQL Server"
    configs["mssql"]["server"] = "35.154.120.224,1433"
    configs["mssql"]["database"] = "FalcaPOSProdDB"
    configs["mssql"]["user"] = "SHAKTI_USER"
    configs["mssql"]["password"] = "sHAKTI2023$!"
    
    print("\n--------------Enter TARGET MONGO-DB connection details--------------")
    configs['mongodb'] = {}
    #Host
    print("Enter host:")
    configs['mongodb']['host'] = input()
    
    #Port number
    print("Enter port:")
    configs['mongodb']['port'] = int(input())
    
    print("Auth not enabled by default")
    
    #DB name
    print("Enter db name:")
    configs['mongodb']['database'] = input()

    with open(config_path, 'w') as yaml_file:
        yaml.dump(configs, yaml_file, default_flow_style=False)

    print("------------------------DB Configurations finished------------------")


def setAutoDBConfig(config_folder="../config", config_file="db-config.yaml"):
    if not os.path.exists(config_folder):
        os.makedirs(config_folder)

    config_path = os.path.join(config_folder, config_file)

    configs = {}
    #ist = pytz.timezone('Asia/Kolkata')
    current_datetime = datetime.datetime.now()
    formatted_date = current_datetime.strftime('%Y-%m-%d')
    print(formatted_date)
    configs["mongodb"] = {}
    
    configs["mongodb"]["database"] = "suggi_prod_"+formatted_date
    configs["mongodb"]["host"] = "localhost"
    configs["mongodb"]["port"] = 27017
    
    configs["mssql"] = {}

    configs["mssql"]["driver"] = "ODBC Driver 18 for SQL Server"
    configs["mssql"]["server"] = "35.154.120.224,1433"
    configs["mssql"]["database"] = "FalcaPOSProdDB"
    configs["mssql"]["user"] = "SHAKTI_USER"
    configs["mssql"]["password"] = "sHAKTI2023$!"
    with open(config_path, 'w') as yaml_file:
        yaml.dump(configs, yaml_file, default_flow_style=False)

    print("------------------------DB Configurations finished------------------")

    


def selectTables(config_folder="../config", config_file="transformation-rules.yaml"):
    
    mysql_cursor = mysql_connector.get_mssql_connection().cursor()
    mysql_cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
    mysql_tables = mysql_cursor.fetchall()
    print(mysql_tables)
    mysql_tabs = []
    config = load_config()
    for (i,item) in enumerate(mysql_tables):
        if item[0] in ["tbllogintime","'Supplier Codes$'","Seeds$","Fertlizers$","CPC$","Organics$","SpecilityNutrients$","ToolsImplements$","MissingCategory$","MissingCategory2$","'Falca POS Reports$'","Sheet1$","StateCodes$"]:
            continue
        mysql_tabs.append({i+1 : item[0]})
        #print(i,item)
    print(mysql_tables)
    print(processTableNames(mysql_tabs))

    config_path = os.path.join(config_folder, config_file)
    configs = {}
    
    option = getOption()
    print(option)
    mysql_tabs_list = [list(tab.values())[0] for tab in mysql_tabs]
    
    if (option == 1):
        configs['source_table_names'] = mysql_tabs_list
    elif (option == 2):
        print("Enter the numbers of tables you want to include(Separate numbers by a comma)")
        tables_to_include_indexes = input_numbers_to_array(input())
        tables_to_include = process_tables_to_include(mysql_tabs_list, tables_to_include_indexes)
        configs['source_table_names'] = tables_to_include
    elif (option == 3):
        print("Enter the numbers of tables DO NOT you want to include(Separate numbers by a comma)")
        tables_to_exclude_indexes = input_numbers_to_array(input())
        tables_to_include = process_tables_to_exclude(mysql_tabs_list, tables_to_exclude_indexes)
        configs['source_table_names'] = tables_to_include
    else:
        configs['source_table_names'] = []
    print("----------------------------------------------------------------")
    print("Enter the prefix you want to append to mongo collection names:")
    prefix = input()
    configs["dest_collection_names"] = [prefix+i for i in configs['source_table_names']]

    with open(config_path, 'w') as yaml_file:
        yaml.dump(configs, yaml_file, default_flow_style=False)
    print("Saved configs")


def autoSelectTables(config_folder="../config", config_file="transformation-rules.yaml"):
    mysql_cursor = mysql_connector.get_mssql_connection().cursor()
    mysql_cursor.execute("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'")
    mysql_tables = mysql_cursor.fetchall()
    mysql_tabs = []
    config = load_config()
    for (i,item) in enumerate(mysql_tables):
        if item[0] in ["tbllogintime","'Supplier Codes$'","Seeds$","Fertlizers$","CPC$","Organics$","SpecilityNutrients$","ToolsImplements$","MissingCategory$","MissingCategory2$","'Falca POS Reports$'","Sheet1$","StateCodes$"]:
            continue
        mysql_tabs.append({i+1 : item[0]})
        #print(i,item)
    #print(processTableNames(mysql_tabs))

    config_path = os.path.join(config_folder, config_file)
    configs = {}
    
    mysql_tabs_list = [list(tab.values())[0] for tab in mysql_tabs]
    configs['source_table_names'] = mysql_tabs_list
    configs['dest_collection_names'] = ["mig_"+table for table in mysql_tabs_list]
    with open(config_path, 'w') as yaml_file:
        yaml.dump(configs, yaml_file, default_flow_style=False)
    print("Saved configs")
        


def get_password():
    try:
        password = getpass.getpass(prompt="Enter password: ")
        return password
    except KeyboardInterrupt:
        return None

def processTableNames(mysql_tabs):
    keys = [list(tab.keys())[0] for tab in mysql_tabs]
    values = [list(tab.values())[0] for tab in mysql_tabs]
    df = pd.DataFrame({'Sl No': keys, 'Table': values})
    table = tabulate(df, headers='keys', tablefmt='pretty',showindex=False)
    return table




def getOption(options=["Select all tables", "Enter table numbers to include","Enter table numbers to exclude"]):
    while True:
        print("Please select an option regarding your desired action for the tables:")
        for i, option in enumerate(options, start=1):
            print(f"{i}. {option}")
        
        try:
            choice = int(input("Enter the number of your choice: "))
            if 1 <= choice <= len(options):
                return choice 
            else:
                print("Invalid option. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def input_numbers_to_array(input_string):
    input_list = input_string.split(',')
    try:
        num_array = [int(item.strip()) for item in input_list]
        return num_array
    except ValueError:
        return None

def process_tables_to_include(main_list, sub_list):
    result = [main_list[i] for i in range(len(main_list)) if i+1 in sub_list]
    return result

def process_tables_to_exclude(main_list, sub_list):
    result = [main_list[i] for i in range(len(main_list)) if i+1 not in sub_list]
    return result