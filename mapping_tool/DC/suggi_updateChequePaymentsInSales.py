import pymongo
from tqdm import tqdm

client = pymongo.MongoClient("mongodb://localhost:27017")  

from load_config import load_config
config = load_config()
source_db = client[config["suggi_source"]]
target_db = client[config["target"]]


pipeline = [
      {
        "$lookup": {
            "from": "mig_tblchequepayment",
            "localField": "cheque_ref",
            "foreignField": "id",
            "as": "chequeDetails"
        }
        
      },
    {"$unwind": "$chequeDetails"}
]


try:
    payments = list(source_db.mig_tblsale_payment_mapping.aggregate(pipeline))
    progress_bar = tqdm(total=len(payments),desc="Processing")
    for payment in payments:
        print(payment['sale_ref'])
        

    
except Exception as e:
    print(f"Error: {e}")


client.close()
