import pymongo

# 1. Connect to your MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017")  # Replace with your MongoDB connection string

from load_config import load_config
config = load_config()
source_db = client[config["source"]]
target_db = client[config["target"]]


# 2. Define the aggregation pipeline
pipeline = [
    {
        "$lookup": {
            "from": "mig_tblproducttype_manufacture_mapping",
            "localField": "producttype_manufacture_ref",
            "foreignField": "id",
            "as": "mapping"
        }
    },
    {
        "$unwind": "$mapping"
    },
    {
        "$lookup": {
            "from": "mig_tblproducttype",
            "localField": "mapping.producttype_ref",
            "foreignField": "id",
            "as": "sub_category"
        }
    },
    {
        "$unwind": "$sub_category"
    },
    {
        "$lookup": {
            "from": "mig_tblmanufacture",
            "localField": "mapping.manufacture_ref",
            "foreignField": "id",
            "as": "manufacturer"
        }
    },
    {
        "$unwind": "$manufacturer"
    },
    {
        "$lookup": {
            "from": "mig_tblcategory",
            "localField": "sub_category.category_ref",
            "foreignField": "id",
            "as": "category"
        }
    },
    {
        "$unwind": "$category"
    },
    {
        "$project": {
            "mapping": 0
        }
    }
]

# 3. Execute the aggregation and create a new collection
result = list(source_db.mig_tblproduct.aggregate(pipeline))
target_db.tblproduct.insert_many(result)

# Close the MongoDB connection
client.close()
