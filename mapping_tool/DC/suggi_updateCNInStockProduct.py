from pymongo import MongoClient
from tqdm import tqdm
import numpy as np
import pandas as pd
from load_config import load_config
config = load_config()

client = MongoClient("mongodb://localhost:27017")  
db = client[config['target']]



# Define the collection names
tblstockproduct_collection = db['tblstockproduct']
tblstockproducinvoice_collection = db['tblstockproduct_invoice']

result = list(tblstockproduct_collection.find())
progress_bar = tqdm(total=len(result), desc="Processing")

# Iterate over documents in tblstockproduct and update them with corresponding tblstockproduct CN
for document in result:
    tblstockproduct_collection.update_one({"_id":document["_id"]},{"$set":{"cnStockproduct":0}})
    progress_bar.update(1)
progress_bar.close()


excel_file_path = './invoice_data/Book.xlsx'

df = pd.read_excel(excel_file_path)
df.fillna('', inplace=True)

progress_bar = tqdm(total=len(df), desc="Processing")

rows_as_dicts = df.to_dict(orient='records')
# print(rows_as_dicts)
print("All CN values set to 0")
print("Updating CN values according to excel")

dd = {}

# Get Distributed lot details 
for row in rows_as_dicts:
    try:
        #checking if there is any data which has null data 
        if row['CN Number'] != '':
                if row['CN Number'] not in dd:
                    dd[row['CN Number']] = []
                data = tblstockproduct_collection.find_one({"id":int(row['stockproduct_ref'])})
                invoice=data['invoice']['invoiceno']
                product= data['product_ref']
                temp=list(tblstockproduct_collection.find({"invoice.invoiceno":invoice , "product_ref":product}))
                for lots in temp:
                    lot_data = {}
                    lot_data['Lot']=lots['id']
                    lot_data['Total']=lots['subqty']*lots['rate']
                    if row['CN Number'] in dd:
                        if lot_data not in dd[row['CN Number']]:
                            dd[row['CN Number']].append(lot_data)

    except:
        continue
    
    progress_bar.update(1)
progress_bar.close()

# print(dd)

# Total value of a invoice 
dict={}
for key, value in dd.items():
    sum=0
    for val in value:
        sum=sum+val['Total']
    dict[key]=sum

print(dict)

CN_details={}
for row in rows_as_dicts:
    try:
        if row['CN Number'] not in CN_details:
            CN_details[row['CN Number']]=row['CN total']
    except:
        continue


for key,value in dd.items():
    Lot_Total_Amount=dict[key]
    CN_Amount = CN_details[key]
    for val in value:
        Lot_Total=val['Total']
        CN_StockProduct_Amount= (Lot_Total/Lot_Total_Amount)*CN_Amount
        data = tblstockproduct_collection.find_one({"id":int(val['Lot'])})
        tblstockproduct_collection.update_one({"id":int(val['Lot'])},{"$set":{"cnStockproduct":CN_StockProduct_Amount +  data['cnStockproduct']}})
    
# Close the MongoDB connection
client.close()
