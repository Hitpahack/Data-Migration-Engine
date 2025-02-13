import pymongo
from tqdm import tqdm
from halo import Halo

client = pymongo.MongoClient("mongodb://localhost:27017")  

from load_config import load_config

config = load_config()
source_db = client[config["siri_temp_db"]]
target_db = client[config["target"]]


pipeline = [
    {
        "$lookup": {
            "from": "tblConsumerTransaction",
            "localField": "LoadId",
            "foreignField": "LoadId",
            "as": "ConsumerTransaction"
        }
    },
    {
        "$unwind": {
            "path": "$ConsumerTransaction",
            "preserveNullAndEmptyArrays": True
        }
    },
    {
        "$unwind": {
            "path":"$LoadDetails.userDetails",
            "preserveNullAndEmptyArrays": True
        }
    },
    {
        "$lookup": {
            "from": "tblBillingTransaction",
            "localField": "LoadDetails.userDetails.InvoiceId",
            "foreignField": "InvoiceID",
            "as": "billingTransactions"
        }
    },
    {
        "$unwind": {
            "path":"$billingTransactions",
            "preserveNullAndEmptyArrays": True
        }
    },
    {
        "$lookup": {
            "from": "users",
            "localField": "LoadDetails.userDetails.UserId",
            "foreignField": "_id",
            "as": "userProfile"
        }
    },
   {
        "$unwind": {
            "path":"$userProfile",
            "preserveNullAndEmptyArrays": True
        }
    },
    {
        "$lookup": {
            "from": "users",
            "localField": "BuyerId",
            "foreignField": "_id",
            "as": "buyerProfile"
        }
    },
    {
        "$unwind": {
            "path":"$buyerProfile",
            "preserveNullAndEmptyArrays": True
        }
    },
    {
        "$lookup": {
            "from": "tblFalcaCenters",
            "localField": "HonorDistrict",
            "foreignField": "CenterName",
            "as": "CenterDetails"
        }
    },
    {
        "$unwind": {
            "path":"$CenterDetails",
            "preserveNullAndEmptyArrays": True
        }
    },
    {
        "$group": {
            "_id": "$_id",
            "BuyerId": {"$first": "$BuyerId"},
            "PurchaseOrderId": {"$first": "$PurchaseOrderId"},
            "LoadId": {"$first": "$LoadId"},
            "InvoiceID": {"$first": "$InvoiceID"},
            "LoadDetails": {"$first": "$LoadDetails"},
            "TransportInformation": {"$first": "$TransportInformation"},
            "HonorState": {"$first": "$HonorState"},
            "HonorDistrict": {"$first": "$HonorDistrict"},
            "UserType": {"$first": "$UserType"},
            "Status": {"$first": "$Status"},
            "TransactionType": {"$first": "$TransactionType"},
            "LoadType": {"$first": "$LoadType"},
            "AssignType": {"$first": "$AssignType"},
            "createdBy": {"$first": "$createdBy"},
            "BiltyStatus": {"$first": "$BiltyStatus"},
            "CreatedAt": {"$first": "$CreatedAt"},
            "EwayBill": {"$first": "$EwayBill"},
            "BuyerGRNImgId": {"$first": "$BuyerGRNImgId"},
            "BuyerGRNDeduction": {"$first": "$BuyerGRNDeduction"},
            "CenterType":{"$first": "$CenterDetails.CenterType"},
            # "ConsumerTransaction":{"$first":{ 
            # "$mergeObjects":["$ConsumerTransaction",{'buyerName':{"$concat":["$buyerProfile.profile.Name","_",{"$toString":"$buyerProfile.profile.Phone.Primary"}]}}]
            # }},
            "BuyerName" : {"$first":{"$concat":["$buyerProfile.profile.Name","_",{"$toString":"$buyerProfile.profile.Phone.Primary"}]}},
            "BuyerOnboardingDate":{"$first":"$buyerProfile.createdAt"},
            "ConsumerTransaction":{"$first":"$ConsumerTransaction"},
            "users": {
                    "$push": 
                            {
                                "userDetails":{"$mergeObjects":["$LoadDetails.userDetails",{"userName" :{"$concat":["$userProfile.profile.Name","_",{"$toString":"$userProfile.profile.Phone.Primary"}]},"UserOnboardingDate":"$userProfile.createdAt"}]},
                                "billingTransaction": "$billingTransactions"
                            },
                        
                },
        },
    },
    {
        "$project":
        {
            "_id": 1,
            "BuyerId": 1,
            "PurchaseOrderId": 1,
            "LoadId": 1,
            "InvoiceID": 1,
            "LoadDetails": 1,
            "TransportInformation": 1,
            "HonorState": 1,
            "HonorDistrict": 1,
            "UserType": 1,
            "Status": 1,
            "TransactionType": 1,
            "LoadType": 1,
            "AssignType": 1,
            "createdBy": 1,
            "BiltyStatus": 1,
            "CreatedAt": 1,
            "EwayBill": 1,
            "BuyerGRNImgId": 1,
            "BuyerGRNDeduction":1,
            "LoadDetails":{
            "$mergeObjects":["$LoadDetails",{'users':"$users"}]
            },
            "ConsumerTransaction":1,
            "BuyerName":1,
            "BuyerOnboardingDate":1,
            "CenterType":1
            
        }
    },
    {
        "$project":{
            "LoadDetails.userDetails":0
        }
    }
    
]

try:
    spinner = Halo(text='RUNNING AGGREGATION PIPELINE...', spinner='dots2')  # Choose from various spinners
    spinner.start()
    cursor = source_db.tblTransaction.aggregate(pipeline)
    spinner.stop()
    print("\n")
    progress_bar = tqdm(total=len(list(source_db.tblTransaction.find())),desc="Processing")
    count_404 = 0 
    for row in cursor:
        # print("Hello")
        if "users" in row["LoadDetails"].keys():
            for index,row_users in enumerate(row["LoadDetails"]["users"]):
                if "userDetails" in row["LoadDetails"]["users"][index].keys():
                    if "Unit" in row_users["userDetails"].keys():
                        if row_users["userDetails"]["Unit"] == "KG":
                            row["LoadDetails"]["users"][index]['userDetails']['Quantity'] =  row["LoadDetails"]["users"][index]['userDetails']['Quantity'] / 100
                            
                            row["LoadDetails"]["users"][index]['userDetails']['Price'] =  row["LoadDetails"]["users"][index]['userDetails']['Price'] * 100
                            
                            row["LoadDetails"]["users"][index]['userDetails']['Unit'] =  "Qtl"
                        
                        if row_users['userDetails']["Unit"] == "Ton":
                            row["LoadDetails"]["users"][index]['userDetails']['Quantity'] =  row["LoadDetails"]["users"][index]['userDetails']['Quantity'] * 10

                            row["LoadDetails"]["users"][index]['userDetails']['Price'] =  row["LoadDetails"]["users"][index]['userDetails']['Price'] / 10
                            
                            row["LoadDetails"]["users"][index]['userDetails']['Unit'] =  "Qtl"
                    if "Soot" not in row_users["userDetails"].keys():
                        row_users["userDetails"]["Soot"] = 0.0
                    
                    misc_charges = 0
                    
                    if "Miscellaneous" in row_users["userDetails"].keys() and row_users["userDetails"] is not None:
                        row["LoadDetails"]["users"][index]['userDetails']["HamaliDeduct"] = 0
                        row["LoadDetails"]["users"][index]['userDetails']["LivesDeduct"] = 0
                        row["LoadDetails"]["users"][index]['userDetails']["TransportationCharges"]= 0
                        row["LoadDetails"]["users"][index]['userDetails']["WeighBridgeExpense"]= 0
                        row["LoadDetails"]["users"][index]['userDetails']["APMCCess"]= 0
                        row["LoadDetails"]["users"][index]['userDetails']["EmptyGunnyBag"]= 0
                        row["LoadDetails"]["users"][index]['userDetails']["BuyerDeductions"]= 0
                        
                        
                        for row_misc in row_users["userDetails"]["Miscellaneous"]:
                            if row_misc["Type"] != "Advance" and row_misc["Type"] != "Finance Advance":
                                misc_charges += row_misc["Charges"]
                            
                            if row_misc["Type"] == "Hamali Deduct":
                                row["LoadDetails"]["users"][index]['userDetails']["HamaliDeduct"] = row_misc["Charges"]            
                            if row_misc["Type"] == "Lives Deduct":
                                row["LoadDetails"]["users"][index]['userDetails']["LivesDeduct"] = row_misc["Charges"]            
                            if row_misc["Type"] == "Transportation Charges":
                                row["LoadDetails"]["users"][index]['userDetails']["TransportationCharges"] = row_misc["Charges"]            
                            if row_misc["Type"] == "Weigh Bridge Expense":
                                row["LoadDetails"]["users"][index]['userDetails']["WeighBridgeExpense"] = row_misc["Charges"]            
                            if row_misc["Type"] == "Empty Gunny Bag":
                                row["LoadDetails"]["users"][index]['userDetails']["EmptyGunnyBag"] = row_misc["Charges"]            
                            if row_misc["Type"] == "APMC Cess":
                                row["LoadDetails"]["users"][index]['userDetails']["APMCCess"] = row_misc["Charges"]
                            if row_misc["Type"] == "Buyer Deductions":
                                if  row_misc["Charges"] < 100000:
                                    misc_charges += row_misc["Charges"]
                                row["LoadDetails"]["users"][index]['userDetails']["BuyerDeductions"] = row_misc["Charges"]  

                                                        
                    row["LoadDetails"]["users"][index]['userDetails']['TotalMiscCharges'] = misc_charges

        if "Unit" in row["LoadDetails"].keys():
                if row["LoadDetails"]["Unit"] == "KG" :
                    
                    row["LoadDetails"]["Quantity"] =  row["LoadDetails"]["Quantity"] / 100
                                
                    row["LoadDetails"]["UnLoadQuantity"] =  row["LoadDetails"]["UnLoadQuantity"] / 100
                            
                    row["LoadDetails"]["FreeQty"] =  row["LoadDetails"]["FreeQty"] / 100
                            
                    row["LoadDetails"]["BiltyFreeQty"] =  row["LoadDetails"]["BiltyFreeQty"] / 100

                    if "WeighBridgeQty" in row['LoadDetails']:
                        row["LoadDetails"]["WeighBridgeQty"] =  row["LoadDetails"]["WeighBridgeQty"] / 100

                    row["LoadDetails"]["Unit"] =  "Qtl"
                    
                if row["LoadDetails"]["Unit"] == "Ton":
                    row["LoadDetails"]["Quantity"] =  row["LoadDetails"]["Quantity"] * 10
                                
                    row["LoadDetails"]["UnLoadQuantity"] =  row["LoadDetails"]["UnLoadQuantity"] * 10
                            
                    row["LoadDetails"]["FreeQty"] =  row["LoadDetails"]["FreeQty"] * 10
                            
                    row["LoadDetails"]["BiltyFreeQty"] =  row["LoadDetails"]["BiltyFreeQty"] * 10

                    if "WeighBridgeQty" in row['LoadDetails']:
                        row["LoadDetails"]["WeighBridgeQty"] =  row["LoadDetails"]["WeighBridgeQty"] * 10
                            
                    row["LoadDetails"]["Unit"] =  "Qtl"
        if "ConsumerTransaction" in dict(row).keys() and row['ConsumerTransaction'] is not None:
                    
            if row["ConsumerTransaction"]["Unit"] == "KG":
                        
                row["ConsumerTransaction"]["InvoiceQty"] =  row["ConsumerTransaction"]["InvoiceQty"] / 100

                row["ConsumerTransaction"]["UnLoadQuantity"] =  row["ConsumerTransaction"]["UnLoadQuantity"] / 100

                row["ConsumerTransaction"]["PriceQuote"] =  row["ConsumerTransaction"]["PriceQuote"] * 100
                        
                row["ConsumerTransaction"]["Unit"] = "Qtl"

            if row["ConsumerTransaction"]["Unit"] == "Ton":
                        
                row["ConsumerTransaction"]["InvoiceQty"] =  row["ConsumerTransaction"]["InvoiceQty"] * 10

                row["ConsumerTransaction"]["UnLoadQuantity"] =  row["ConsumerTransaction"]["UnLoadQuantity"] * 10

                row["ConsumerTransaction"]["PriceQuote"] =  row["ConsumerTransaction"]["PriceQuote"] / 10
                        
                row["ConsumerTransaction"]["Unit"] = "Qtl"
        target_db.siri_tblTransaction.insert_one(dict(row))
        progress_bar.update(1)
    progress_bar.close()
except Exception as e:
    print(f"Error: {e}")


client.close()
