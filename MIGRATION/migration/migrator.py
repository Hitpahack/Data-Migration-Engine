import yaml
from replicator import * 
def load_config(yaml_file="../config/transformation-rules.yaml"):
    with open(yaml_file, "r") as file:
        config = yaml.safe_load(file)
    return config

def startMigration():
    config = load_config()
    for mysql_table, mongo_collection in zip(config['source_table_names'],config['dest_collection_names']):
        migrate_table_to_mongo_collection(mysql_table,processCollectioName(mongo_collection))
    #migrate_table_to_mongo_collection("tblpurchaseorder_supplier_product_mapping","tblpurchaseorder_supplier_product_mapping")
    print("----------------------------------------END----------------------------------")

def processCollectioName(col_name):
    return col_name.replace("$","") 