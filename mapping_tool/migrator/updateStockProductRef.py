import pymongo
from tqdm import tqdm

client = pymongo.MongoClient("mongodb://localhost:27017/")  # Update the connection string as needed

from load_config import load_config
config = load_config()
source_db = client[config["source"]]
target_db = client[config["target"]]

sales = list(target_db.tblsale.find())
progress_bar = tqdm(total=len(sales),desc="Processing")
    
for sale_doc in sales:
    for product in sale_doc["product"]:
        # Find the corresponding stock_product document
        stock_product = target_db.tblstockproduct.find_one({"id": product["product_ref"]})
        if stock_product:
            # Update the product with the _stock_product_ref field
            product["_stock_product_ref"] = stock_product["_id"]
    progress_bar.update(1)

    
    # Update the document in the tblsale collection
    target_db.tblsale.update_one({"_id": sale_doc["_id"]}, {"$set": {"product": sale_doc["product"]}})
progress_bar.close()