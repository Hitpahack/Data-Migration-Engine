from pymongo import MongoClient
from datetime import datetime
import yaml
from halo import Halo
import logging
import socket


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except Exception as e:
        print(f"Error: {e}")
        return None


# Connection to MongoDB
client = MongoClient('mongodb://localhost:27017')  # Replace with your MongoDB connection string
username = "meteorsa"
password = "falca2016"
# ------------------USE THIS CLIENT WITH CAUTION! (CLIENT FOR SIRI-PROD DB)----------------
siri_prod_db_client = MongoClient(f'mongodb://{username}:{password}@3.7.70.184:27017')  
#----------------------------------------------------------------------------------------

from load_config import load_config
config = load_config()


# PREPARING DB FROM SIRI-PROD DB IS ++ READ-ONLY ++-----------------------------------------------
siri_prod_db = siri_prod_db_client["meteor"] 
# -------------------------------------------------------------------------------------------

with open("../config/source-target.yaml", 'w') as yaml_file:
    config["siri_source"] = "meteor_"+datetime.now().strftime("%Y-%m-%d")
    yaml.dump(config, yaml_file, default_flow_style=False)
    print("Source Db config saved successfully")

siri_temp_db_name = config["siri_source"][:6]+"FY23-24_"+config["siri_source"][7:]
siri_temp_db = client[siri_temp_db_name]

with open("../config/source-target.yaml", 'w') as yaml_file:
    config["siri_temp_db"] = siri_temp_db_name
    yaml.dump(config, yaml_file, default_flow_style=False)
    print("Temp Db config saved successfully")

def fetch_data_from_collection(collection_name, start_date, end_date):
    
    # FETCHING EACH COLLECTION FROM SIRI-PROD DB IS ++ READ-ONLY ++-----------------------------------------------
    collection = siri_prod_db[collection_name] 
    # -------------------------------------------------------------------------------------------

    query = {
        'CreatedAt': {'$gte': start_date, '$lte': end_date}
    }

    # FETCHING EACH COLLECTION DATA FROM SIRI-PROD DB IS ++ READ-ONLY ++-----------------------------------------------
    result = list(collection.find(query))
    # -------------------------------------------------------------------------------------------
    
    # Log the query details
    timestamp = datetime.now()
    local_ip = get_local_ip()
    local_host_name = socket.gethostname()
    log_message = f"Find() Query executed on collection {collection_name} on meteor DATABASE present at 3.7.70.184 at {timestamp} by {local_ip} {local_host_name}"
    logging.info(log_message)
    

    return result

# Function to fetch data from all collections in a date range
def fetch_data_from_date_range(start_date, end_date):
    
    # FETCHING COLLECTION NAMES FROM SIRI-PROD DB IS ++ READ-ONLY ++-----------------------------------------------
    collections = siri_prod_db.list_collection_names() 
    # -------------------------------------------------------------------------------------------
    
    spinner = Halo(text='CREATING CURRENT FINANCIAL YEAR DB...', spinner='dots2')  # Choose from various spinners
    spinner.start()

    for collection_name in collections:
        try : 
            collection_data = fetch_data_from_collection(collection_name, start_date, end_date)
            siri_temp_db[collection_name].insert_many(collection_data)
        except:
            continue
    spinner.stop()
    print("Successfully created current year DB!")
# Example usage
start_date = datetime(2023, 4, 1, 0, 0, 0)
end_date = datetime.now()

fetch_data_from_date_range(start_date, end_date)
