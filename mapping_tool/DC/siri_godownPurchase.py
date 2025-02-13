import pymongo
from tqdm import tqdm

client = pymongo.MongoClient("mongodb://localhost:27017")  

from load_config import load_config

config = load_config()
source_db = client[config["target"]]
target_db = client[config["target"]]



try:
    cursor = source_db.siri_tblTransaction.find({"UserType":"Godown"})
    progress_bar = tqdm(total=len(list(source_db.tblTransaction.find())),desc="Processing")
    for row in cursor:
        try:
            target_db.siri_tblGodownPurchase.insert_one(dict(row))
        except Exception as e:
            print(f"Error: {e}")
        progress_bar.update(1)
    progress_bar.close()
except Exception as e:
    print(f"Error: {e}")

client.close()
