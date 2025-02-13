import pymongo
from tqdm import tqdm

from load_config import load_config



client = pymongo.MongoClient("mongodb://localhost:27017")  

config = load_config()
source_db = client[config["suggi_source"]]
target_db = client[config["target"]]



try:
    cursor = source_db.mig_tblstockproduct_invoice.find()
    rows = list(cursor)
    progress_bar = tqdm(total=len(rows),desc="Processing")
    for row in rows:
        target_db.tblstockproduct_invoice.insert_one(row)
        progress_bar.update(1)
    progress_bar.close()
except Exception as e:
    print(f"Error: {e}")


client.close()
