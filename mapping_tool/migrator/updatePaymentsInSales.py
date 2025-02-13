import pymongo
from tqdm import tqdm

client = pymongo.MongoClient("mongodb://localhost:27017")  

from load_config import load_config
config = load_config()
source_db = client[config["source"]]
target_db = client[config["target"]]

try:
    payments = list(source_db.mig_tblsale_payment_mapping.find())
    progress_bar = tqdm(total=len(payments),desc="Processing")
    for payment in payments:
        target_db.tblsale.update_one({"id":payment['sale_ref']},{"$set":{"payment":payment}})
        progress_bar.update(1)

    progress_bar.close()
except Exception as e:
    print(f"Error: {e}")


client.close()
