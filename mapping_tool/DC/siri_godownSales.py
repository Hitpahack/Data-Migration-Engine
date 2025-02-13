import pymongo
from tqdm import tqdm

client = pymongo.MongoClient("mongodb://localhost:27017")  

from load_config import load_config

config = load_config()
source_db = client[config["target"]]
target_db = client[config["target"]]

try:
    cursor = source_db.siri_tblTransaction.find().sort("CreatedAt",1)
    for row in cursor:
        try:    
            obj=[]
            Psum=0
            
            # if row["UserType"] == "Godown":
            #     print("Godown Purchase")
            #     continue

            if row["Status"] in ["Cancelled","Rejected","Deleted"] :
                print("Skipped")
                continue

            for temp in row['LoadDetails']['users']:
                data=list(source_db.users.find({"_id":temp['userDetails']['UserId']}))
                if data[0]['profile']['Role'] == "Godown":

                    inventory=list(source_db.siri_tblGodownInventory.find({"GodownID":temp['userDetails']['UserId'],"InventoryStatus":"Stock","userDetails.CropName":temp['userDetails']['CropName']}).sort("CreatedAt",1)) 

                
                    if (temp['userDetails']['UserId']=="SbCLLCGRyHRGgAvTR" and temp['userDetails']['CropName'] == "Maize(Corn)Seed"):
                        print(temp['userDetails']['Quantity'],row["InvoiceID"])

                    sum=0;
                    lot=[]
                    for data in inventory:
                        sum=sum+data['StockAmount']
                        if temp['userDetails']['Quantity'] >= sum:
                            result = target_db.siri_tblGodownInventory.update_one({"_id":data['_id']},{"$set":{"InventoryStatus":"Sold","StockAmount":0}})
                            data['ProcurredQty']=data['StockAmount']

                            
                            Psum=Psum+data['ProcurredQty']
                            obj.append(data)

                        elif temp['userDetails']['Quantity'] < sum:
                            data['ProcurredQty']=temp['userDetails']['Quantity']-(sum-data['StockAmount'])


                            Psum=Psum+data['ProcurredQty']
                            result = target_db.siri_tblGodownInventory.update_one({"_id":data['_id']},{"$set":{"StockAmount":data['StockAmount']-data['ProcurredQty']}})
                            obj.append(data)
                            break
                    
                else:
                    obj.append(temp)
                    Psum=Psum+ temp['userDetails']['Quantity']
                
            row['LoadDetails']['users']=obj
            row['LoadDetails']['TotalProcurredQty']=Psum
            target_db.siri_tblGodownSales.insert_one(row)
        except Exception as e:
                # print(f"Error: {e}")
                continue
    
except Exception as e:
    print(f"Error: {e}")


client.close()
