import pymongo
from tqdm import tqdm
from halo import Halo

client = pymongo.MongoClient("mongodb://localhost:27017")  

from load_config import load_config

config = load_config()
source_db = client[config["target"]]
target_db = client[config["target"]]
siri_temp_db = client[config["siri_temp_db"]]
skip_count = 0
result = source_db.siri_tblTransaction.find()

spinner = Halo(text='Updating Selling prices in siri_tblTransaction...', spinner='dots2')  # Choose from various spinners
spinner.start()
    
for row in result:
    po = siri_temp_db.tblPurchaseOrder.find_one({"PurchaseOrderId":row["PurchaseOrderId"]})
    try:
        for crop in po["PurchaseOrderDetail"]:
            if row["UserType"] != "Godown":
                if "userDetails" in row["LoadDetails"]["users"][0].keys():
                    if crop["CropName"] == row["LoadDetails"]["users"][0]["userDetails"]["CropName"]:
                        sp = crop["Price"]
                        unit = crop["Unit"]
                        if unit == "KG":
                            sp = sp*100
                        if unit == "Ton":
                            sp = sp/10
                        target_db.siri_tblTransaction.update_one({"_id":row["_id"]},{"$set":{"SellingPrice":sp}})
        
    except Exception as e:
        skip_count = skip_count+1
        continue
spinner.stop()

print(f"{skip_count} rows skipped")

print("Updated Selling prices!")

client.close()
