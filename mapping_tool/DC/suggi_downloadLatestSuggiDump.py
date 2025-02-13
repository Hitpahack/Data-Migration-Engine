import boto3
import os
import zipfile
import pytz
import datetime
import shutil
from pymongo import MongoClient
import subprocess
import yaml
from tqdm import tqdm


# Set your AWS credentials and region


# Initialize a session using Amazon S3
session = boto3.Session(
   
)
s3 = session.client('s3')

def getCurrentDayDateString():
    #ist = pytz.timezone('Asia/Kolkata')
    current_datetime = datetime.datetime.now()
    formatted_date = current_datetime.strftime('%Y-%m-%d')
    return formatted_date

def delete_folder(folder_path):
    try:
        # Remove the folder and its contents recursively
        shutil.rmtree(folder_path)
        print(f'Successfully deleted the folder and its contents: {folder_path}')
    except OSError as e:
        print(f'Error: {e}')

def getLatestS3Objet(bucket_name):
    objects = s3.list_objects_v2(Bucket=bucket_name)
    latest_timestamp = None
    latest_object = None
    for obj in objects.get('Contents', []):
        timestamp = obj['LastModified']
        if latest_timestamp is None or timestamp > latest_timestamp:
            latest_timestamp = timestamp
            latest_object = obj
    
    if latest_object : 
        return latest_object
    else:
        return None

def load_migration_config(yaml_file="../../migration-config.yaml"):
    with open(yaml_file, "r") as file:
        config = yaml.safe_load(file)
    return config



def mongoRestore(SOURCE_PATH):
    migration_configs = load_migration_config()
    paths = migration_configs['paths']

    print(paths)
    
    try:
        restore_db_name = f"{SOURCE_PATH}temp".replace(".zip",'')
        command = [paths['mongorestore-path'], "--db", restore_db_name, f"./dumps/{SOURCE_PATH}/".replace(".zip","")]
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during backup: {e}")
    finally:
        print("Mongodb restored successfully")

        configs = {}
        configs["suggi_source"] = restore_db_name
        configs["target"] = restore_db_name.replace("suggi_prod_","shakti").replace("temp",'mapped')

        with open("../config/source-target.yaml", 'w') as yaml_file:
            yaml.dump(configs, yaml_file, default_flow_style=False)
            print("Saved source target configs")
            

if __name__ == "__main__":
    if not os.path.exists("./dumps"):
        os.makedirs("./dumps")
        print(f"Directory './dumps' created.")
    else:
        print(f"Directory ./dumps already exists.")
    
    BUCKET_NAME = "shakti-data"
    SOURCE_PATH = getLatestS3Objet(BUCKET_NAME)['Key']

    print("Downloading latest dump from S3...")

    DESTINATION_PATH = "dumps/" + SOURCE_PATH
    print(DESTINATION_PATH)

    # Get the size of the S3 object for progress tracking
    s3_object = s3.head_object(Bucket=BUCKET_NAME, Key=SOURCE_PATH)
    total_size = s3_object['ContentLength']

    with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
        def callback(bytes_amount):
            pbar.update(bytes_amount)

        s3.download_file(BUCKET_NAME, SOURCE_PATH, DESTINATION_PATH, Callback=callback)

    print("Download completed.")
    print("Extracting ZIP file...")

    with zipfile.ZipFile(DESTINATION_PATH, 'r') as zip_ref:
        zip_ref.extractall(f"./dumps/{SOURCE_PATH.replace('.zip', '')}")

    print("ZIP extraction completed.")
    print("Restoring data to MongoDB...")
    
    mongoRestore(SOURCE_PATH)

    print("Data restore completed.")
    
    delete_folder("./dumps")



