import pymongo
from tqdm import tqdm

client = pymongo.MongoClient("mongodb://localhost:27017")  

from load_config import load_config

config = load_config()
source_db = client[config["target"]]
# target_db = client[config["target"]]

try:
    cursor = source_db.siri_tblGodownSales.find().sort("CreatedAt",1)
    for row in cursor:
        try:    
            


            if row["Status"] in ["Cancelled","Rejected","Deleted"] :
                print("Skipped")
                continue


            new_users =[]
            for temp in row['LoadDetails']['users']:
                data=list(source_db.users.find({"_id":temp['userDetails']['UserId']}))
                if data[0]['profile']['Role'] == "Godown" and "GodownStart" not in temp["LoadId"]:

                    resolved_data = source_db.siri_tblGodownSales.find({"LoadId":temp['LoadId']})
                    resolved_data_arr = []
                    for data in resolved_data:
                        resolved_data_arr.append(data)

                    cross_check = 0

                    for lot in resolved_data_arr[0]["LoadDetails"]["users"]:
                        newProcurredqty = temp['ProcurredQty']*(lot['ProcurredQty']/resolved_data_arr[0]["LoadDetails"]["TotalProcurredQty"])
                        cross_check += newProcurredqty
                        lot['ProcurredQty'] = newProcurredqty
                        new_users.append(lot)   

                    if cross_check > 0 :
                        print(row["InvoiceID"],temp["LoadId"])                 
                else:
                    new_users.append(temp)


            source_db.siri_tblGodownSales.update_one({"_id":row['_id']},{"$set":{"LoadDetails.users":new_users}})

        except Exception as e:
                print(f"Error: {e}")
                continue
    
except Exception as e:
    print(f"Error: {e}")


client.close()
