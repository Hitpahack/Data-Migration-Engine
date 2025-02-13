import pymongo
from tqdm import tqdm
import time
import multiprocessing as mp
from itertools import islice
from load_config import load_config

def process_chunk(chunk):
    client = pymongo.MongoClient("mongodb://localhost:27017")
    config = load_config()
    source_db = client[config["suggi_source"]]
    target_db = client[config["target"]]

    for row in chunk:
        row = source_db.mig_tblcustomer.find_one({"_id": row["_id"]})  # Get full document

        # Perform lookup and unwind manually
        address_doc = source_db.mig_tbladdress.find_one({"id": row['address_ref']})
        row['address'] = address_doc

        customer_uid = f"{row['name']}_{row['phone']}"
        row['customer_uid'] = customer_uid

        result = list(source_db.mig_tblsale.find({"customer_ref": row['id']},
                                                 {"_id": 0, "invoicedate": 1})
                      .sort("invoicedate", 1).limit(1))
        if result:
            data = result[0]['invoicedate']
        else:
            data = row["createddatetime"]
            
        row['onboarding_date'] = data
        target_db.tblcustomer.insert_one(row)

    client.close()

def chunked_iterable(iterable, size):
    """Yield successive n-sized chunks from an iterable."""
    iterator = iter(iterable)
    for first in iterator:
        yield [first] + list(islice(iterator, size - 1))

if __name__ == "__main__":
    config = load_config()
    client = pymongo.MongoClient("mongodb://localhost:27017")
    source_db = client[config["suggi_source"]]
    
    # Define the number of processes
    num_processes = 10
    chunk_size = 1000  # Adjust based on memory and performance needs

    start = time.time()

    total_docs = source_db.mig_tblcustomer.count_documents({})
    all_docs = source_db.mig_tblcustomer.find({}, {"_id": 1})  # Only get _id to reduce memory usage

    print(f"Total documents to process: {total_docs}")

    chunks = list(chunked_iterable(all_docs, chunk_size))

    with mp.Pool(num_processes) as pool:
        with tqdm(total=total_docs, desc="Processing") as progress_bar:
            for _ in tqdm(pool.imap_unordered(process_chunk, chunks), total=len(chunks)):
                progress_bar.update(chunk_size)

    end = time.time()
    print(f"Execution time: {(end - start) * 10**3:.2f} ms")
    print("------Script 1 finished--------")

    client.close()
