import pymongo
from tqdm import tqdm
import datetime

def pad_integer(number):
    number_str = str(number)
    if len(number_str) == 1:
        padded_number = f"000{number_str}"
    elif len(number_str) == 2:
        padded_number = f"00{number_str}"
    elif len(number_str) == 3:
        padded_number = f"0{number_str}"
    else:
        padded_number = number_str

    return padded_number
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Update the connection string as needed

from load_config import load_config
config = load_config()
source_db = client[config["suggi_source"]]
target_db = client[config["target"]]

lots = list(target_db.tblstockproduct.find())
progress_bar = tqdm(total=len(lots),desc="Processing")


po_prefix = "99"
po_count = 0

for lot in lots:
    po = {}    
    if lot['invoice']['po_ref'] is None :
      po_id_to_find = int(po_prefix+pad_integer(lot["invoice"]["supplier_ref"])+pad_integer(lot["store_ref"]))
      combined_ref_to_find = str(po_id_to_find)+"-"+str(lot['product_ref'])  
      existing_po =  target_db.tblpurchaseorder.find_one({"Id" : po_id_to_find})
      target_db.tblstockproduct.update_one({"id":lot['id']},{"$set":{"combined_po_product_ref":combined_ref_to_find}})
      if existing_po:
        existing_combined_ref = target_db.tblpurchaseorder.find_one({"products.combined_po_product_ref":combined_ref_to_find})
        if lot['invoice']['invoicedate'] is not None and lot['invoice']['invoicedate'] < existing_po['podate']:
           podate=lot['invoice']['invoicedate'] 
        else:
           podate=existing_po['podate']

        if existing_combined_ref:
            products = existing_combined_ref['products']
            for index,product in enumerate(products):
               if product['combined_po_product_ref'] == combined_ref_to_find:
                products[index]['availableqty'] = product['availableqty'] + lot['subqty']
                products[index]['qty'] = product['qty'] + lot['subqty']
                products[index]['receivedqty'] = product['receivedqty'] + lot['subqty']

            target_db.tblpurchaseorder.update_one({"Id" :existing_po['Id'] ,"products.combined_po_product_ref":combined_ref_to_find},{"$set":{"products": products, "podate":podate}})
        else :             
            result = target_db.tblpurchaseorder.update_one({"Id" :existing_po['Id']},{"$push":{"products":{ "product_ref":lot['product_ref'],"qty":lot['subqty'],"availableqty":lot['subqty'],"receivedqty":lot['subqty'],"combined_po_product_ref" : combined_ref_to_find}}})
            target_db.tblpurchaseorder.update_one({"Id" :existing_po['Id'] },{"$set":{"podate":podate}})   
            
      else:
        po_id = int(po_prefix+pad_integer(lot["invoice"]["supplier_ref"])+pad_integer(lot["store_ref"]))  
        po['Id'] = po_id
        po['pono'] = "PO/FS/"+(po_prefix)+"/"+pad_integer(lot["invoice"]["supplier_ref"])+"/"+pad_integer(lot["store_ref"])
        
        if lot['invoice']['invoicedate'] is None:
            po['podate'] = datetime.datetime.now()
        else:
            po['podate'] = lot['invoice']['invoicedate']

        po['store_ref'] = lot["store_ref"]
        po['status'] = "dummy"
        po['remarks'] = "dummy PO"
        po['type'] = "dummy"
        po['createdby_ref'] = None
        po['paymentstatus'] = None
        products = []
        products.append({"product_ref":lot['product_ref'],"qty":lot['subqty'],"availableqty":lot['subqty'],"receivedqty":lot['subqty'],"combined_po_product_ref" : combined_ref_to_find})
        po['products'] = products
        po['supplier_details'] = target_db.tblsupplier.find_one({"id":lot["invoice"]["supplier_ref"]})
        result = target_db.tblpurchaseorder.insert_one(po)
        po_count = po_count + 1
    progress_bar.update(1)
print("Number of New POs created:")
print(po_count)
progress_bar.close()