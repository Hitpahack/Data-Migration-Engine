import pymongo
from tqdm import tqdm
from halo import Halo

client = pymongo.MongoClient("mongodb://localhost:27017")  

from load_config import load_config

config = load_config()
db = client[config["target"]]

try:
    cursor = db.siri_tblTransaction.find()
    for row in cursor:
        if "users" in row["LoadDetails"].keys():
            bilty_pv = []
            for index,row_users in enumerate(row["LoadDetails"]["users"]):
                if "userDetails" in row["LoadDetails"]["users"][index].keys():
                    if "InvoiceId" in row["LoadDetails"]["users"][index]["userDetails"].keys() and len(row["LoadDetails"]["users"][index]["userDetails"]["InvoiceId"]) > 0:
                        if row["LoadDetails"]["users"][index]["userDetails"]["InvoiceId"][-1].isalpha():
                            bilty_pv.append(row["LoadDetails"]["users"][index]["userDetails"]["InvoiceId"][:-1])
            
            
            if bilty_pv != []:
                bilty_pv = set(bilty_pv)            
                new_users = []
                for index,row_users in enumerate(row["LoadDetails"]["users"]):
                    if "userDetails" in row["LoadDetails"]["users"][index].keys():
                        if "InvoiceId" in row["LoadDetails"]["users"][index]["userDetails"].keys() and row["LoadDetails"]["users"][index]["userDetails"]["InvoiceId"] not in bilty_pv:
                            new_users.append(row_users)
                            
                print(row["_id"])
                db.siri_tblTransaction.update_one({"_id":row["_id"]},{"$set":{"LoadDetails.users":new_users}})

except Exception as error:
    print(error)