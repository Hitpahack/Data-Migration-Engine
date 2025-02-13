from pymongo import MongoClient
from tqdm import tqdm
import pandas as pd
from load_config import load_config
config = load_config()

client = MongoClient("mongodb://localhost:27017")  
db = client[config['target']]



# Define the collection names
tblstockproduct_collection = db['tblstockproduct']

result = list(tblstockproduct_collection.find())
progress_bar = tqdm(total=len(result), desc="Processing")

# Iterate over documents in tblstockproduct and update them with corresponding tblstockproduct CN
for document in result:
    tblstockproduct_collection.update_one({"_id":document["_id"]},{"$set":{"cnStockproduct":0}})
    progress_bar.update(1)
progress_bar.close()


excel_file_path = './invoice_data/CN-INVOICE.xlsx'
df = pd.read_excel(excel_file_path)
progress_bar = tqdm(total=len(df), desc="Processing")

rows_as_dicts = df.to_dict(orient='records')
print("All CN values set to 0")
print("Updating CN values according to excel")
for row in rows_as_dicts:
    try:
        if isinstance(row['stockproduct_ref'], (int, float, complex)): 
            data = tblstockproduct_collection.find_one({"id":int(row['stockproduct_ref'])})
            tblstockproduct_collection.update_one({"id":int(row['stockproduct_ref'])},{"$set":{"cnStockproduct": row["CN-stockproduct"] + data['cnStockproduct'] }})
    except:
        print(row)
    
    progress_bar.update(1)
progress_bar.close()

# Close the MongoDB connection
client.close()
