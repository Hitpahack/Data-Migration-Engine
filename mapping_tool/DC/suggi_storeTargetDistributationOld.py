from pymongo import MongoClient
from tqdm import tqdm
import pandas as pd
from load_config import load_config
config = load_config()
from IPython import embed

client = MongoClient("mongodb://localhost:27017")  
db = client[config['target']]
sale_collection = db["tblsaleMaster"]

excel_file_path = './store_data/Suggi Targets.xlsx'
df = pd.read_excel(excel_file_path)
rows_as_dicts = df.to_dict(orient='records')

result = list(sale_collection.find())

# progress_bar = tqdm(total=len(result), desc="Processing")
# for document in result:
#     sale_collection.update_one({"_id":document["_id"]},{"$set":{"product.storeTargetPerProduct":0}})
#     progress_bar.update(1)
# progress_bar.close()

for row in rows_as_dicts:
    try:
        store = row["Store ref"]
        print("running for ", store)
        for key in row.keys():
            if key in ["Store ref","Store","Sub-Category"]:
                continue
            else:
                print(key,row[key])
                if float(row[key]) == 0:
                    continue
                sale_data = list(sale_collection.find({ 
                                "$and":[
                                    {"$expr": { "$eq": [{ "$month": "$createddate" }, int(key.month)] }},
                                    {"$expr": { "$eq": [{ "$year": "$createddate" },int(key.year)]}},
                                    {"storeDetails.id":int(store)}
                                ]
                            }))
                monthly_sale = 0
                sub_category_gross = {}
                for i,sale in enumerate(sale_data):
                    for j,product in enumerate(sale["product"]):
                        if product["purchaseProductDetails"]["sub_category"]["name"] in sub_category_gross.keys():
                            sub_category_gross[product["purchaseProductDetails"]["sub_category"]["name"]]+= product["sellingprice"]*product["soldqty"]
                        else:
                             sub_category_gross[product["purchaseProductDetails"]["sub_category"]["name"]]= product["sellingprice"]*product["soldqty"]
                    monthly_sale += sale["grosstotal"]
                tally = 0
                for sale in sale_data:
                    products = []
                    for product in sale["product"]:
                        if "sub_category" in product["purchaseProductDetails"].keys() and product["purchaseProductDetails"]["sub_category"]["name"] == row["Sub-Category"]:
                            storeTargetPerProduct = (product["sellingprice"]*product["soldqty"])*float(row[key])/sub_category_gross[product["purchaseProductDetails"]["sub_category"]["name"]]
                            product["storeTargetPerProduct"] = storeTargetPerProduct
                            tally += storeTargetPerProduct
                        products.append(product)
                    sale_collection.update_one({"_id":sale["_id"]},{"$set":{"product":products}})

                print(key,monthly_sale,row[key]-tally)
        
    except Exception as error:
        print(error)
    


    