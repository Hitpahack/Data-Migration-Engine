import subprocess

subprocess.run(['python', "siri_downloadLatestSIRI-DB.py"])
subprocess.run(['python', "siri_createCurrentFyDB.py"])
subprocess.run(['python', "siri_usersMigration.py"])
subprocess.run(['python', "siri_tblTransactionMigration.py"])
subprocess.run(['python', "siri_updateSellingPriceIntblTransaction.py"])   
