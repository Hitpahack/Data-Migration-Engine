import pymongo
from tqdm import tqdm
client = pymongo.MongoClient("mongodb://localhost:27017")  
from load_config import load_config
config = load_config()
source_db = client[config["suggi_source"]]
target_db = client[config["target"]]

import time

pipeline = [
    {
        "$lookup": {
            "from": "mig_tbladdress",
            "localField": "address_ref",
            "foreignField": "id",
            "as": "address"
        },
    },
    {"$unwind":"$address"},
    {
        "$lookup": {
            "from": "mig_tblvillagename",
            "localField": "address.village_ref",
            "foreignField": "id",
            "as": "village"
        }
    },
    {
        "$unwind": {
            "path":"$village",
            "preserveNullAndEmptyArrays": True  
        }
    },
    {
        "$lookup": {
            "from": "mig_tblpincode",
            "localField": "village.pincode_ref",
            "foreignField": "id",
            "as": "pincode"
        }
    },
    {
        "$unwind": {
            "path":"$pincode",
            "preserveNullAndEmptyArrays": True  
        }
    }
    
]

try:
    start = time.time()
    cursor = source_db.mig_tblcustomer.aggregate(pipeline).batch_size(35)
    end = time.time()

    print(f"EXECUTION TIME {end-start* 10**3} ")

    print("Hello")
    print("------Script 1 started--------")
    progress_bar = tqdm(total=len(list(source_db.mig_tblcustomer.find())),desc="Processing")
    # data={}
    for index,row in enumerate(cursor):
        customer_uid = row['name']+"_"+row['phone']
        row['customer_uid'] = customer_uid
        result=list(source_db.mig_tblsale.find({"customer_ref":row['id']},{"_id":0 ,"invoicedate":1}).sort({"invoicedate":1}).limit(1));
        if len(result)>0: 
            data=result[0]['invoicedate']
        else:
            data=row["createddatetime"]        
        row['onboarding_date']=data
        target_db.tblcustomer.insert_one(dict(row))
        progress_bar.update(1)

    progress_bar.close()
    print("------Script 1 finished--------")
except Exception as e:
    print(f"Error: {e}")


client.close()
