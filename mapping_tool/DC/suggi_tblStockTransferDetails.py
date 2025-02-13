import pymongo
from tqdm import tqdm
from halo import Halo



client = pymongo.MongoClient("mongodb://localhost:27017")  

from load_config import load_config

config = load_config()
source_db = client[config["suggi_source"]]
target_db = client[config["target"]]



pipeline = [
    {"$lookup": {
        "from": "mig_tblstocktransfer_product_mapping",
        "localField": "stp_ref",
        "foreignField": "id",
        "as": "stocktransfer_product_mapping",
    }},
    {"$unwind": "$stocktransfer_product_mapping"},
    {"$lookup": {
        "from": "mig_tblstockproduct",
        "localField": "stockproduct_ref",
        "foreignField": "id",
        "as": "stockproduct",
    }},
    {"$unwind": "$stockproduct"},
    {"$lookup": {
        "from": "mig_tblstocktransfer",
        "localField": "stocktransfer_product_mapping.st_ref",
        "foreignField": "id",
        "as": "stocktransfer",
    }},
    {"$unwind": "$stocktransfer"},
    {"$lookup": {
        "from": "mig_tblproduct",
        "localField": "stocktransfer_product_mapping.product_ref",
        "foreignField": "id",
        "as": "product",
    }},
    {"$unwind": "$product"},
    {"$lookup": {
        "from": "mig_tblstore",
        "localField": "stocktransfer.store_ref",
        "foreignField": "id",
        "as": "fromstore",
    }},
    {"$unwind": "$fromstore"},
    {"$lookup": {
        "from": "mig_tblstocktransfer_store_product_mapping",
        "localField": "stocktransfer_fromstore_ref",
        "foreignField": "id",
        "as": "stocktransfer_store_product_mapping",
    }},
    {"$unwind": "$stocktransfer_store_product_mapping"},
    {"$lookup": {
        "from": "mig_tblstore",
        "localField": "stocktransfer_store_product_mapping.fromstore_ref",
        "foreignField": "id",
        "as": "to_store",
    }},
    {"$unwind": "$to_store"},
    {
     "$group": {
            "_id": "$_id",
            "received_lot": {"$first": "$stockproduct_ref"},
            "lotqty": {"$first": "$lotqty"},
            "product": {
                    "$mergeObjects":{
                        "_id": "$product._id",
                        "id": "$product.id",
                        "name": "$product.name",
                        "unit": "$product.unit",
                        "qty": "$stocktransfer_product_mapping.qty",
                        "rate":"$stockproduct.rate",
                        "sellingprice":"$stockproduct.sellingprice"
                    }
            },  
            "stockTransferDetails": {
                    "$mergeObjects":{
                        "_id": "$stocktransfer._id",
                        "id": "$stocktransfer.id",
                        "stock_transfer_no": "$stocktransfer.stno",
                        "stock_transfer_date": "$stocktransfer.stdate",
                        "status": "$stocktransfer.status",          
                        "createddatetime": "$stocktransfer.createddatetime",          
                        
                    }
            },
            "fromStore": {
                    "$mergeObjects":{
                        "_id": "$fromstore._id",
                        "id": "$fromstore.id",
                        "name": "$fromstore.name",
                    }
            },
            "toStore": {
                    "$mergeObjects":{
                        "_id": "$to_store._id",
                        "id": "$to_store.id",
                        "name": "$to_store.name",
                    }
            },
            "transportDetails": {
                    "$mergeObjects":{
                        "_id": "$stocktransfer_store_product_mapping._id",
                        "id": "$stocktransfer_store_product_mapping.id",
                        "others": "$stocktransfer_store_product_mapping.others",
                        "transportcharges": "$stocktransfer_store_product_mapping.transportcharges",
                        "stock_transfer_receiptno": "$stocktransfer_store_product_mapping.streceiptno",
                        "stock_transfer_receiptdate": "$stocktransfer_store_product_mapping.streceiptdate",
                    }
            },
     },
    },    
]



try:
    spinner = Halo(text='RUNNING AGGREGATION PIPELINE ON tblstocktransfer...', spinner='dots2')  # Choose from various spinners
    spinner.start()
    cursor = source_db.mig_tblstocktransfer_product_stockproduct_mapping.aggregate(pipeline)
    spinner.stop()
    progress_bar = tqdm(total=len(list(source_db.mig_tblstocktransfer.find())),desc="Processing")
    for row in cursor:
        target_db.tblStockTransfer.insert_one(dict(row))
        progress_bar.update(1)
    progress_bar.close()
except Exception as e:
    print(f"Error: {e}")

client.close()
