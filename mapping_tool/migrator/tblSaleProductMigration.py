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
            "from": "mig_tblsale_product_price_mapping",
            "localField": "id",
            "foreignField": "sale_ref",
            "as": "product"
        }
        
    }
]


try:
    cursor = source_db.mig_tblsale.aggregate(pipeline).batch_size(35)
    progress_bar = tqdm(total=len(list(source_db.mig_tblsale.find())),desc="Processing")
    for index,row in enumerate(cursor):
        target_db.tblsale.insert_one(dict(row))
        progress_bar.update(1)
    progress_bar.close()
except Exception as e:
    print(f"Error: {e}")


client.close()
