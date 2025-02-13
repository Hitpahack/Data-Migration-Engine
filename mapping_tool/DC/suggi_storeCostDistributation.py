from pymongo import MongoClient
from tqdm import tqdm
import pandas as pd
from load_config import load_config
config = load_config()

client = MongoClient("mongodb://localhost:27017")  
db = client[config['target']]
sale_collection = db["tblsale"]

excel_file_path = './store_data/Store Costing.xlsx'
df = pd.read_excel(excel_file_path)
rows_as_dicts = df.to_dict(orient='records')

result = list(sale_collection.find())
progress_bar = tqdm(total=len(result), desc="Processing")
for document in result:
    sale_collection.update_one({"_id":document["_id"]},{"$set":{"storeCost":0}})
    progress_bar.update(1)
progress_bar.close()

for row in rows_as_dicts:
    try:
        store = row["Store_ref"]
        print("running for ", store)
        for key in row.keys():
            if key in ["Store_ref","Store"]:
                continue
            else:
                sale_data = list(sale_collection.find({ 
                                "$and":[
                                    {"$expr": { "$eq": [{ "$month": "$createddate" }, int(key.month)] }},
                                    {"$expr": { "$eq": [{ "$year": "$createddate" },int(key.year)]}},
                                    {"store_ref":int(store)}
                                ]
                            }))
                monthly_sale = 0
                for sale in sale_data:
                    monthly_sale += sale["grosstotal"]
                
                tally = 0
                for sale in sale_data:
                    storeCostPerSale = sale['grosstotal']*float(row[key])/monthly_sale
                    sale_collection.update_one({"_id":sale["_id"]},{"$set":{"storeCost":storeCostPerSale}})
                    tally += storeCostPerSale
                
                print(key,row[key],monthly_sale,tally)
    except Exception as error:
        print(error)
    