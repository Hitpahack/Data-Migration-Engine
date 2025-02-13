import pymongo
from tqdm import tqdm



client = pymongo.MongoClient("mongodb://localhost:27017")  

from load_config import load_config

config = load_config()
source_db = client[config["suggi_source"]]
target_db = client[config["target"]]

# pipeline = [
#     {
#         "$lookup": {
#             "from": "mig_tblsupplier_addresss_mapping",
#             "localField": "id",
#             "foreignField": "supplier_ref",
#             "as": "mapping"
#         }
#     },
#     {
#         "$unwind": "$mapping"
#     },    
# ]


try:
    result = list(source_db.mig_tblsupplier.find())
    progress_bar = tqdm(total=len(result), desc="Processing")

    for row in result:
        target_db.tblsupplier.insert_one(row)
        progress_bar.update(1)
    progress_bar.close()
except Exception as e:
    print(f"Error: {e}")


client.close()
