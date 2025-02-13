import yaml
from pymongo import MongoClient

def load_config(yaml_file="../config/db-config.yaml"):
    with open(yaml_file, "r") as file:
        config = yaml.safe_load(file)
    return config

def get_mongodb_connection():
    config = load_config()['mongodb']
    client = MongoClient(
        host=config["host"],
        port=config["port"],
        authSource=config["database"]
    )
    db = client[config["database"]]
    return db

