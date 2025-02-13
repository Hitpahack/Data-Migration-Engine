import pymongo
from tqdm import tqdm


# MongoDB connection settings
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
from load_config import load_config
config = load_config()
source_db = client[config["source"]]
target_db = client[config["target"]]

tblcustomer = target_db["tblcustomer"]
tblstore = target_db["tblstore"]
tbluser = target_db["tbluser"]
tblsale = target_db["tblsale"]

tab = tblsale.find()
progress_bar = tqdm(total=29540, desc="Processing")

# Iterate through tblsale documents
for sale_doc in tab:
    try:
        _customer_ref = tblcustomer.find_one({"id":sale_doc['customer_ref']},{"_id":1})    
        _store_ref = tblstore.find_one({"id":sale_doc['store_ref']},{"_id":1})    
        _saleby_ref = tbluser.find_one({"id":sale_doc['saleby_ref']},{"_id":1})
        print(_customer_ref)
        print(_store_ref)
        print(_saleby_ref)
        print("+=======================================+")    
        tblsale.update_one({"_id": sale_doc["_id"]}, {"$set": {"_customer_ref": _customer_ref['_id'],"_store_ref":_store_ref['_id'],"_saleby_ref" : _saleby_ref['_id']}})
    except :
        continue
    progress_bar.update(1)
    
progress_bar.close()
# Close the MongoDB client
client.close()
