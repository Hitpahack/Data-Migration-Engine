import pymongo
from tqdm import tqdm


# MongoDB connection settings
client = pymongo.MongoClient("mongodb://127.0.0.1:27017")
from load_config import load_config
config = load_config()
source_db = client[config["suggi_source"]]
target_db = client[config["target"]]

mig_tblcreditnote_stockproduct_mappings = source_db['mig_tblcreditnote_stockproduct_mappings']
tblcreditnote = target_db['tblcreditnote']
tblstockproduct = target_db['tblstockproduct']


mappings = list(mig_tblcreditnote_stockproduct_mappings.find())
progress_bar = tqdm(total=len(mappings), desc="Processing")

# Iterate through tblsale documents
for mapping in mappings:
    try:
        _stockproduct_ref = tblstockproduct.find_one({"id":mapping['stockproduct_ref']},{"_id":1})    
        _creditnote_ref = tblcreditnote.find_one({"id":mapping['creditnote_ref']},{"_id":1})    
        print(_stockproduct_ref)
        print(_creditnote_ref)
        print("+=======================================+")    
        target_db.tblcreditnote_stockproduct_mappings.insert_one({"_stockproduct_ref":_stockproduct_ref['_id'],"_creditnote_ref":_creditnote_ref['_id']})
    except :
        continue
    progress_bar.update(1)
    
progress_bar.close()
# Close the MongoDB client
client.close()
