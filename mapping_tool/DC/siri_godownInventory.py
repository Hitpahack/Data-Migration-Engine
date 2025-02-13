import pymongo,csv,datetime
from tqdm import tqdm

client = pymongo.MongoClient("mongodb://localhost:27017")  

from load_config import load_config

config = load_config()
source_db = client[config["target"]]
target_db = client[config["target"]]
temp_db = client[config["siri_temp_db"]]


lot_id = 1
with open('./store_data/godownHeadstart.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)
        data ={}
        data["lotId"] = lot_id
        data["StockAmount"] = float(row["Quantity"])
        data["CreatedAt"] = datetime.datetime.strptime("2023-04-01 00:00:00.000000","%Y-%m-%d %H:%M:%S.%f")
        data["InventoryStatus"]="Stock"
        data["userDetails"]= {
            "CropName":row["CropName"],
            "UserId":row["GodownID"],
            "Price":float(row["Price"]),
            "Unit":"Qtl",
            "InvoiceId": "FY2324GodownStart"
        }
        data["GodownID"]=row["GodownID"]

        gname = temp_db.users.find({"_id":data["GodownID"]})
        for dt in gname:
            data['GodownName'] = " ".join(dt["profile"]["Name"].split("_"))
        data['initialStock'] = data['StockAmount']
        data['LoadId'] = str(lot_id)+"/FY2324GodownStart"
        data["billingTransaction"]={}
        target_db.siri_tblGodownInventory.insert_one(data)
        lot_id += 1

try:
    cursor = source_db.siri_tblGodownPurchase.find({"Status":"UnLoaded"}).sort('CreatedAt',1)
    i=lot_id
    j=0
    for row in cursor:
        try:    
            Total=0
            for temp in row['LoadDetails']['users']:   
                if 'Quantity' in temp['userDetails'].keys():
                    Total += temp['userDetails']['Quantity']; 

            for temp in row['LoadDetails']['users']: 
                if 'Quantity' in temp['userDetails'].keys():              
                    data={}
                    data['lotId']=i
                    i=i+1
                    data['userDetails']=temp['userDetails']
                    data['billingTransaction']={}
                    data['InventoryStatus']='Stock'
                    data['StockAmount']=(temp['userDetails']['Quantity']/Total)*row['LoadDetails']['UnLoadQuantity']
                    data['CreatedAt'] = row["CreatedAt"]
                    data['GodownID'] = row["BuyerId"]
                    data['GodownName'] = " ".join(row["BuyerName"].split("_")[:-1])
                    data['initialStock'] = data['StockAmount']
                    data['LoadId'] = row['LoadId']

                    
                    # if data['GodownID'] == "SbCLLCGRyHRGgAvTR" and temp['userDetails']["CropName"] == "Maize(Corn)Seed":

                    #     print(j,",",data['StockAmount'],",",temp['userDetails']['Quantity'],",",Total,row['LoadDetails']['UnLoadQuantity'])
                    #     j+=1

                    target_db.siri_tblGodownInventory.insert_one(data)

            if round(Total,2) != round(row['LoadDetails']['UnLoadQuantity'],2):
                target_db.siri_WrongInventoryData.insert_one(row)

        except Exception as e:
            print(f"Error: {e}")
except Exception as e:
    print(f"Error: {e}")

client.close()
