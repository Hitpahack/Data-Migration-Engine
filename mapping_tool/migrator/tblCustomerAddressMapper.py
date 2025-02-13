import pymongo
from tqdm import tqdm




client = pymongo.MongoClient("mongodb://localhost:27017")  

from load_config import load_config

config = load_config()
source_db = client[config["source"]]
target_db = client[config["target"]]



pipeline = [
    {
        "$lookup": {
            "from": "mig_tbladdress",
            "localField": "address_ref",
            "foreignField": "id",
            "as": "address"
        }
        
    },
    {"$unwind": "$address"}
]


try:
    cursor = source_db.mig_tblcustomer.aggregate(pipeline).batch_size(35)
    print("------Script 1 started--------")
    progress_bar = tqdm(total=len(list(source_db.mig_tblcustomer.find())),desc="Processing")
    for index,row in enumerate(cursor):
        target_db.tblcustomer.insert_one(dict(row))
        progress_bar.update(1)
    progress_bar.close()
    print("------Script 1 finished--------")
except Exception as e:
    print(f"Error: {e}")


client.close()
