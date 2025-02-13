import pymongo
from tqdm import tqdm
import logging
from datetime import datetime
import socket
from load_config import load_config


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



# Configure logging
logging.basicConfig(filename='../logs/siri_prod_read_logs.txt', level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s')

client = pymongo.MongoClient("mongodb://localhost:27017")  

username = "meteorsa"
password = "falca2016"
# ------------------USE THIS CLIENT WITH CAUTION! (CLIENT FOR SIRI-PROD DB)----------------
siri_prod_db_client = pymongo.MongoClient(f'mongodb://{username}:{password}@3.7.70.184:27017')  
#----------------------------------------------------------------------------------------


config = load_config()

# PREPARING DB FROM SIRI-PROD DB IS ++ READ-ONLY ++-----------------------------------------------
siri_prod_db = siri_prod_db_client["meteor"] 
# -------------------------------------------------------------------------------------------

target_db = client[config["target"]]
temp_db = client[config["siri_temp_db"]]


try:
    
    # FIND QUERY ON SIRI-PROD DB IS ++ READ-ONLY ++-----------------------------------------------
    cursor = siri_prod_db.users.find()
    # -------------------------------------------------------------------------------------------
    
    
    # Log the query details
    timestamp = datetime.now()
    local_ip = get_local_ip()
    local_host_name = socket.gethostname()
    log_message = f"Find() Query executed on collection users on meteor DATABASE present at 3.7.70.184 at {timestamp} by {local_ip} {local_host_name}"
    logging.info(log_message)
    
    progress_bar = tqdm(total=86527,desc="Processing")
    for row in cursor:
        target_db.users.insert_one(dict(row))
        temp_db.users.insert_one(dict(row))
        progress_bar.update(1)
    progress_bar.close()
except Exception as e:
    print(f"Error: {e}")

finally:
    client.close()
    siri_prod_db_client.close()
