from pymongo import MongoClient
from tqdm import tqdm

from load_config import load_config
config = load_config()

client = MongoClient("mongodb://localhost:27017")  
db = client[config['target']]

# Define the collection names
tblstockproduct_collection = db['tblstockproduct']
tblstockproduct_invoice_collection = db['tblstockproduct_invoice']

result = list(tblstockproduct_collection.find())
progress_bar = tqdm(total=len(result), desc="Processing")

# Iterate over documents in tblstockproduct and update them with corresponding tblstockproduct_invoice documents
for document in result:
    invoice_ref = document.get('invoice_ref')
    if invoice_ref:
        invoice_document = tblstockproduct_invoice_collection.find_one({'id': invoice_ref})
        transport_charges = 0
        other_charges = 0
        combined_po_product_ref = str(invoice_document["po_ref"])+"-"+str(document["product_ref"])
        if invoice_document['Transportcharges'] != 0:
            transport_charges = ((document.get('rate') * document.get('subqty')) / (invoice_document['total'])) * invoice_document['Transportcharges']
        if invoice_document['others'] != 0:
            other_charges = ((document.get('rate') * document.get('subqty')) / (invoice_document['total'])) * invoice_document['others']
        if invoice_document:
            tblstockproduct_collection.update_one({'_id': document['_id']}, {'$set': {'invoice': invoice_document,'transportCharges':transport_charges,'otherCharges':other_charges,'combined_po_product_ref':combined_po_product_ref}})
      
    progress_bar.update(1)
progress_bar.close()

# Close the MongoDB connection
client.close()
