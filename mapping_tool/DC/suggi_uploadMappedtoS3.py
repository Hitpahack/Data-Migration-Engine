import boto3
import os
from dotenv import load_dotenv
import argparse
import io
import yaml
import subprocess
from pymongo import MongoClient
import zipfile
import shutil

def load_db_config(yaml_file="../config/source-target.yaml"):
    with open(yaml_file, "r") as file:
        config = yaml.safe_load(file)
    return config


def load_environment():
    load_dotenv(".env")

def setupBucket():
    load_environment()
    s3 = boto3.client(
    's3',
    region_name=os.getenv("REGION_NAME"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
    )
    return s3


s3 = setupBucket()
def create_folder_if_not_exists(bucket, folder_name):
    try:
        s3.head_object(Bucket=bucket, Key=f"{folder_name}/")
    except Exception as e:
        s3.put_object(Bucket=bucket, Key=f"{folder_name}/")

def upload_to_s3(zip_file_path, bucket_name):
    object_key = zip_file_path.split("\\")[-1]
    print(object_key)
    print(s3.upload_file(zip_file_path, bucket_name, object_key))

MONGO_DB = load_db_config()["target"]
MONGO_URI = f"mongodb://localhost:27017/{MONGO_DB}"
    
def createMongodump():
    client = MongoClient(MONGO_URI)
    BACKUP_DIR = ".\\dumps\\"
    configs = load_migration_config()
    paths = configs['paths']
    try:
        command = [
            paths['mongodump-path'],
            "--uri", MONGO_URI,
            "--out", BACKUP_DIR,
        ]

        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during backup: {e}")
    finally:
        client.close()

def load_migration_config(yaml_file="../../migration-config.yaml"):
    with open(yaml_file, "r") as file:
        config = yaml.safe_load(file)
    return config



def compressDump(dump_folder_path, output_dir, zip_filename):
    try:
        os.makedirs(output_dir, exist_ok=True)
        full_output_path = os.path.join(output_dir, zip_filename)

        # Create a ZipFile object in write mode
        with zipfile.ZipFile(full_output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through all the files and subdirectories in the given folder
            for root, _, files in os.walk(dump_folder_path):
                for file in files:
                    # Get the full file path
                    file_path = os.path.join(root, file)
                    
                    # Calculate the relative path inside the ZIP archive
                    relative_path = os.path.relpath(file_path, dump_folder_path)
                    
                    # Add the file to the ZIP archive with its relative path
                    zipf.write(file_path, relative_path)
        
        print(f'Successfully created {zip_filename}')
    except Exception as e:
        print(f'Error: {e}')

def delete_folder(folder_path):
    try:
        # Remove the folder and its contents recursively
        shutil.rmtree(folder_path)
        print(f'Successfully deleted the folder and its contents: {folder_path}')
    except OSError as e:
        print(f'Error: {e}')

def deleteUploadedDatabase(MONGO_DB):
    try:
        client = MongoClient(MONGO_URI)
        # Access the specified database
        db = client[MONGO_DB]
        
        # Drop (delete) the database
        client.drop_database(MONGO_DB)
        
        print(f"Database '{MONGO_DB}' has been deleted.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Close the MongoDB client
        client.close()

def updateServerConfig():
    MONGO_DB = load_db_config()["target"]
    MONGO_URI = f"mongodb://localhost:27017/{MONGO_DB}"
    configs = {}
    with open("../../server-config.yaml", 'r') as yaml_file:
        configs = yaml.safe_load(yaml_file)
        print("Reading server config file")
        print(configs)
    with open("../../server-config.yaml", 'w') as yaml_file:
        configs["MONGO_URI"] = MONGO_URI
        yaml.dump(configs, yaml_file, default_flow_style=False)
    print("Server config saved successfully")
        

def executeUpload():
    print(MONGO_DB,MONGO_URI)
    createMongodump()
    print("here")
    compressDump(".\\dumps\\"+MONGO_DB,".\\dumps\\",MONGO_DB+".zip")
    upload_to_s3(".\\dumps\\"+MONGO_DB+".zip","shakti-data")
    delete_folder(".\\dumps")
    updateServerConfig()
    
executeUpload()