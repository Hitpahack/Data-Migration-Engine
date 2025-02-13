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
            "from": "mig_tblTerritory",
            "localField": "territory_ref",
            "foreignField": "id",
            "as": "territory"
        }
    },
    {
        "$unwind": "$territory"
    },
    {
        "$lookup": {
            "from": "mig_tblZone",
            "localField": "territory.zone_ref",
            "foreignField": "id",
            "as": "zone"
        }
    },
    {
        "$unwind": "$zone"
    },
    {
        "$lookup": {
            "from": "mig_tbladdress",
            "localField": "address_ref",
            "foreignField": "id",
            "as": "address"
        }
    },
    {
        "$unwind": "$address"
    },
    {
        "$group":{
            "_id":"$_id",
            "id":{"$first":"$id"},
            "name":{"$first":"$name"},
            "address_ref":{"$first":"$address_ref"},
            "createddate":{"$first":"$createddate"},
            "invoiceformat":{"$first":"$invoiceformat"},
            "lastgeninvoiceno":{"$first":"$lastgeninvoiceno"},
            "isenabled":{"$first":"$isenabled"},
            "parent_ref":{"$first":"$parent_ref"},
            "cashledger":{"$first":"$cashledger"},
            "upiledger":{"$first":"$upiledger"},
            "costcenter":{"$first":"$costcenter"},
            "territory_ref":{"$first":"$territory_ref"},
            "isStore":{"$first":"$isStore"},
            "vertical":{"$first":"$vertical"},
            "territory":{
                            "$first": { 
                                "$mergeObjects":["$territory",{"zone":"$zone"}]
                                }
                        },
            "address":{"$first":"$address"}
        }
    }
]


try:
    result = list(source_db.mig_tblstore.aggregate(pipeline))
    progress_bar = tqdm(total=len(result), desc="Processing")

    for row in result:
        target_db.tblstore.insert_one(row)
        progress_bar.update(1)
    progress_bar.close()
    print("------Script 3 finsihed--------")
    
except Exception as e:
    print(f"Error: {e}")


client.close()
