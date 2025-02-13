from replicator import *
from migrator import *
from initialiser import *
from uploadToS3Bucket import executeUpload
import sys
import schedule
import time

if len(sys.argv) < 2:
    print("Usage: python migration_main.py <mode>")
    print("Mode 1: pass 'auto' to fetch all tables from source and migrate all data")
    print("Mode 2: pass 'manual' to select tables to fetch and migrate")
    sys.exit(1)

arg = sys.argv[1]

def run_migration():
    if arg == "auto":
        printTitle()
        printAbility()
        print("AUTO mode enabled")
        loading_spinner(15, "Please wait", "⠙")
        setAutoDBConfig()
        print("Preparing REPLICATION")
        autoSelectTables()
        startMigration()  # You should define this function
        executeUpload()
    elif arg == "manual":
        printTitle()
        printAbility()
        loading_spinner(15, "Please wait", "⠙")
        get_db_input_and_create_config()  # You should define this function
        print("Preparing REPLICATION")
        selectTables()  # You should define this function
        startMigration()  # You should define this function
    else:
        print("Invalid argument")
        print("Usage: python migration_main.py <mode>")
        print("Mode 1: pass 'auto' to fetch all tables from source and migrate all data")
        print("Mode 2: pass 'manual' to select tables to fetch and migrate")

run_migration()

#run_migration()