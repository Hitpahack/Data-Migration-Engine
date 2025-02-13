import sys
import datetime
import decimal
from tqdm import tqdm


sys.path.append("../")
from mappers import mysql_connector
from mappers import mongodb_connector

def migrate_table_to_mongo_collection(mysql_table_name, mongo_collection_name):
    
    #MySQL cursor
    mysql_cursor = mysql_connector.get_mssql_connection().cursor()
    
    #Mongo Config
    mongo_db = mongodb_connector.get_mongodb_connection()
    mongo_collection = mongo_db[mongo_collection_name]

    # MySQL Query to fetch data from the table
    mysql_query = f"SELECT * FROM {mysql_table_name}"
    mysql_cursor.execute(mysql_query)

    # Fetch all rows from MySQL Table
    mysql_rows = mysql_cursor.fetchall()
    # Iterate through MySQL rows and insert into MongoDB
    print(f"Migrating table {mysql_table_name} -> {mongo_collection_name}")
    progress_bar = tqdm(total=len(mysql_rows), desc="Processing")
    for index,row in enumerate(mysql_rows):
        processed_row = {key: convert_to_mongodb_compatible(value) for key, value in dict(zip([x[0] for x in mysql_cursor.description], mysql_rows[index])).items()}
        if mysql_table_name == "tblstore":
            if "RSP" in processed_row["name"]:
                processed_row["vertical"] = 'SAMRAT'
            else:
                processed_row["vertical"] = 'SUGGI'
        
        mongo_collection.insert_one(processed_row)
        progress_bar.update(1)
    progress_bar.close()
    print("Finished process\n")

    # Close MySQL and MongoDB connections
    mysql_cursor.close()



# Function to convert data types for MongoDB
def convert_to_mongodb_compatible(value):
    if isinstance(value,datetime.date):
        try : 
            return datetime.datetime.strptime(value.strftime("%Y-%m-%d %H:%M:%S"),"%Y-%m-%d %H:%M:%S")
        except : 
            return None
    elif isinstance(value,decimal.Decimal):
        return float(value)
    elif isinstance(value,datetime.timedelta):
        print("Converted to seconds:",value.total_seconds())
        return value.total_seconds()
    else:
        return value


