import pymongo
from tqdm import tqdm


# MongoDB connection settings
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
from load_config import load_config
config = load_config()
source_db = client[config["suggi_source"]]
target_db = client[config["target"]]

tblcreditnote_stockproduct_mappings = target_db['tblcreditnote_stockproduct_mappings']

mappings = list(tblcreditnote_stockproduct_mappings.find())
progress_bar = tqdm(total=len(mappings), desc="Processing")

# Iterate through tblsale documents
for mapping in mappings:
    try:
        credit_note = dict(target_db.tblcreditnote.find_one({"_id":mapping['_creditnote_ref']}))
        target_db.tblstockproduct.update_one({"_id":mapping['_stockproduct_ref']},{"$set":{"PurchaseCreditNote":credit_note}})
    except :
        continue
    progress_bar.update(1)
    
progress_bar.close()
# Close the MongoDB client
client.close()
