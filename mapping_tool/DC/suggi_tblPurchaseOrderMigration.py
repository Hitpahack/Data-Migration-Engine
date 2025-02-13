import pymongo
from tqdm import tqdm



client = pymongo.MongoClient("mongodb://localhost:27017")  

from load_config import load_config

config = load_config()
source_db = client[config["suggi_source"]]
target_db = client[config["target"]]

pipeline = [
    {
        "$lookup": {
            "from": "mig_tblpurchaseorder_supplier_mapping",
            "localField": "Id",
            "foreignField": "poid_ref",
            "as": "po_supplier_mapping"
        }
    },
    {
        "$unwind": {
            "path":"$po_supplier_mapping",
            "preserveNullAndEmptyArrays": True  
        }
    },
    {
        "$lookup": {
            "from": "mig_tblsupplier",
            "localField": "po_supplier_mapping.supplier_ref",
            "foreignField": "id",
            "as": "supplier_details"
        }
    },
    {
        "$unwind": {
            "path":"$supplier_details",
            "preserveNullAndEmptyArrays": True  
        }
    },
    {
        "$lookup": {
            "from": "mig_tblpurchaseorder_product_mapping",
            "localField": "Id",
            "foreignField": "po_ref",
            "as": "po_product_mapping"
        }
    },
    {
        "$unwind": {
            "path":"$po_product_mapping",
            "preserveNullAndEmptyArrays": True  
        }
    },
    {
        "$lookup": {
            "from": "mig_tblpurchaseorder_supplier_product_mapping",
            "localField": "po_product_mapping.id",
            "foreignField": "poproduct_ref",
            "as": "supplier_product_mapping"
        }
    },
    {
        "$unwind": {
            "path":"$supplier_product_mapping",
            "preserveNullAndEmptyArrays": True  
        }
    },
    {
        "$group": {
            "_id": "$_id",
            "Id": {"$first": "$Id"},
            "pono": {"$first": "$pono"},
            "podate": {"$first": "$podate"},
            "store_ref": {"$first": "$store_ref"},
            "status": {"$first": "$status"},
            "remarks": {"$first": "$remarks"},
            "type": {"$first": "$type"},
            "createdby_ref": {"$first": "$createdby_ref"},
            "createddatetime": {"$first": "$createddatetime"},
            "paymentstatus": {"$first": "$paymentstatus"},
            "products": {
                "$push": {
                    "$mergeObjects": [
                        {
                            "po_product_mapping_mongo_id": "$po_product_mapping._id",
                            "po_product_mapping_id": "$po_product_mapping.id",
                            "po_ref": "$po_product_mapping.po_ref",
                            "product_ref": "$po_product_mapping.product_ref",
                            "qty": "$po_product_mapping.qty",
                            "ftm_qty": "$po_product_mapping.ftm_qty",
                            "grndate": "$po_product_mapping.grndate",
                            "rm_qty": "$po_product_mapping.rm_qty",
                            "rsp": "$po_product_mapping.rsp",
                            "supplier_product_mapping_mongo_id": "$supplier_product_mapping._id",
                            "posupplierid_ref": "$supplier_product_mapping.posupplierid_ref",
                            "poproduct_ref": "$supplier_product_mapping.poproduct_ref",
                            "estimatedprice": "$supplier_product_mapping.estimatedprice",
                            "availableqty": "$supplier_product_mapping.availableqty",
                            "receivedqty": "$supplier_product_mapping.receivedqty",
                            "GST": "$supplier_product_mapping.GST",
                            "eta": "$supplier_product_mapping.eta",
                            "combined_po_product_ref": {"$concat":[{"$toString":"$po_product_mapping.po_ref"},"-",{"$toString":"$po_product_mapping.product_ref"}]},
                            
                        }
                    ]
                }
            },
            "supplier_details": {"$first": "$supplier_details"}
        }
    }
]



try:
    result = list(source_db.mig_tblpurchaseorder.aggregate(pipeline))
    progress_bar = tqdm(total=len(result), desc="Processing")

    for row in result:
        for j,product in enumerate(row["products"]):
            if "availableqty" in product.keys() and "qty" in product.keys() and product["qty"] == 0:
               row["products"][j]["qty"] = product["availableqty"]
        target_db.tblpurchaseorder.insert_one(dict(row))
        progress_bar.update(1)
    progress_bar.close()
except Exception as e:
    print(f"Error: {e}")


client.close()
