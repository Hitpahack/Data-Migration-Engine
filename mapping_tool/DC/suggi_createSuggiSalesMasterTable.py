import pymongo
from tqdm import tqdm
from halo import Halo



client = pymongo.MongoClient("mongodb://localhost:27017")  

from load_config import load_config

config = load_config()
target_db = client[config["target"]]



pipeline = [
    {"$lookup": {
        "from": "tblcustomer",
        "localField": "_customer_ref",
        "foreignField": "_id",
        "as": "customerDetails",
    }},
    {"$unwind": "$customerDetails"},
    {"$lookup": {
        "from": "tblstore",
        "localField": "_store_ref",
        "foreignField": "_id",
        "as": "storeDetails",
    }},
    {"$unwind": "$storeDetails"},
    {"$lookup": {
        "from": "tbluser",
        "localField": "_saleby_ref",
        "foreignField": "_id",
        "as": "userDetails",
    }},
    {"$unwind": "$userDetails"},
    {"$unwind": "$product"},
    {"$lookup": {
        "from": "tblstockproduct",
        "localField": "product._stock_product_ref",
        "foreignField": "_id",
        "as": "stockProductDetails",
    }},
    {"$unwind": "$stockProductDetails"},
    {"$lookup": {
        "from": "tblsupplier",
        "localField": "stockProductDetails.invoice.supplier_ref",
        "foreignField": "id",
        "as": "supplierDetails",
    }},
    {"$unwind": "$supplierDetails"},
    {"$lookup": {
        "from": "tblproduct",
        "localField": "stockProductDetails.product_ref",
        "foreignField": "id",
        "as": "purchaseProductDetails",
    }},
    {"$unwind": "$purchaseProductDetails"},
    {"$group": {
        "_id": "$_id",
        "id": {"$first": "$id"},
        "remarks": {"$first": "$remarks"},
        "invoiceno": {"$first": "$invoiceno"},
        "invoicedate": {"$first": "$invoicedate"},
        "grosstotal": {"$first": "$grosstotal"},
        "discounttype": {"$first": "$discounttype"},
        "discount": {"$first": "$discount"},
        "gst": {"$first": "$gst"},
        "total": {"$first": "$total"},
        "salestype": {"$first": "$salestype"},
        "createddate": {"$first": "$createddate"},
        "SpecialDiscountAmount": {"$first": "$SpecialDiscountAmount"},
        "servicecharges": {"$first": "$servicecharges"},
        "couponcode": {"$first": "$couponcode"},
        "payment": {"$first": "$payment"},
        "customerDetails": {"$first": "$customerDetails"},
        "storeDetails": {"$first": "$storeDetails"},
        "userDetails": {"$first": "$userDetails"},
        "storeCost": {"$first": "$storeCost"},
        "product": {
            "$push": {
                "$mergeObjects": [
                    "$product",
                    {
                        "purchaseProductDetails": "$purchaseProductDetails",
                        "lotDetails": "$stockProductDetails",
                        "supplierDetails": "$supplierDetails"
                    },
                ],
            },
        },
        "totalSoldQty": {"$sum": "$product.soldqty"},
    }},
]


try:
    spinner = Halo(text='RUNNING AGGREGATION PIPELINE ON tblsale...', spinner='dots2')  # Choose from various spinners
    spinner.start()
    cursor = target_db.tblsale.aggregate(pipeline)
    spinner.stop()
    progress_bar = tqdm(total=len(list(target_db.tblsale.find())),desc="Processing")
    for row in cursor:
        target_db.tblsaleMaster.insert_one(dict(row))
        progress_bar.update(1)
    progress_bar.close()
except Exception as e:
    print(f"Error: {e}")


client.close()
