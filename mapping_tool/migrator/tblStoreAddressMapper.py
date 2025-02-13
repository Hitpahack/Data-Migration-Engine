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
    {
        "$unwind": "$address"
    }
]


try:
    result = list(source_db.mig_tblstore.aggregate(pipeline))
    print("------Script 3 started--------")
    progress_bar = tqdm(total=len(result), desc="Processing")

    for row in result:
        target_db.tblstore.insert_one(row)
        progress_bar.update(1)
    progress_bar.close()
    print("------Script 3 finsihed--------")
    
except Exception as e:
    print(f"Error: {e}")


client.close()
