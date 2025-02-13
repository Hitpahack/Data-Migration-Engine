import pymongo
from tqdm import tqdm
import datetime
from load_config import load_config


client = pymongo.MongoClient("mongodb://localhost:27017")  

config = load_config()
source_db = client[config["suggi_source"]]
target_db = client[config["target"]]



try:
    cursor = source_db.mig_tblstockproduct.find()
    rows = list(cursor)
    print("------Script 4 started--------")
    progress_bar = tqdm(total=len(rows),desc="Processing")
    for row in rows:
        if( row["expirydate"] is None or row["expirydate"] > datetime.datetime(2050,12,31,0,0,0)):
            row["expirydate"] = datetime.datetime(2050,12,31,0,0,0)
        target_db.tblstockproduct.insert_one(row)
        progress_bar.update(1)
    progress_bar.close()
    print("------Script 4 finished--------")
except Exception as e:
    print(f"Error: {e}")


client.close()
