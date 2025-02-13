import pymongo,csv
client = pymongo.MongoClient("mongodb://localhost:27017")  


source_db = client["31_3_2023_dump"]


cursor = source_db.tblPurchaseOrder.find({"UserType":"Godown"})

fields =["GodownID","CropName","Price","Quantity","CreatedAt","Unit"]


with open('./store_data/godownHeadstart.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fields)
    writer.writeheader()
    for row in cursor:
        for lot in row["PurchaseOrderDetail"]:
            if (lot['GradeA'] + lot['GradeB'] + lot['GradeC'] > 0):
                print(lot)
                writer.writerow({
                    'GodownID':row['BuyerId'],
                    'CropName': lot['CropName'],
                    'Price': ((lot['GradeAAvgPrice'] + lot['GradeBAvgPrice'] + lot['GradeCAvgPrice'])/3),
                    'Quantity':(lot['GradeA'] + lot['GradeB'] + lot['GradeC']),
                    'CreatedAt':row['CreatedAt'],
                    'Unit':lot['Unit']
                })


        
