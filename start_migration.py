# Schedule the job to run every day at 18:33
#schedule.every(2).minutes.do(run_migration)
import subprocess
import schedule
import time,os
import yaml
def load_migration_config(yaml_file="./migration-config.yaml"):
    with open(yaml_file, "r") as file:
        config = yaml.safe_load(file)
    return config


def run_migration():
    configs = load_migration_config()
    paths = configs['paths']
    os.chdir(paths['migrator-path'])
    subprocess.run(['python', "migration_main.py","auto"])

    os.chdir(paths['mapper-path'])
    subprocess.run(['python', "main.py"])
    
    os.chdir(paths['root-path'])
    subprocess.Popen('pm2 reload 0',shell=True)
    

schedule.every().day.at("21:30:00").do(run_migration)

# run_migration()
while True:
    schedule.run_pending()
    time.sleep(1)
