import subprocess

subprocess.run(['python3', "download.py"])

subprocess.run(['python3', "tblStoreAddressMapper.py"])
subprocess.run(['python3', "tblUserAddressMapper.py"])
subprocess.run(['python3', "tblCustomerAddressMapper.py"])

subprocess.run(['python3', "tblCreditNoteMig.py"])
subprocess.run(['python3', "tblChequepaymentMig.py"])
subprocess.run(['python3', "tblStockProductMig.py"])

subprocess.run(['python3', "tblSaleProductMigration.py"])
subprocess.run(['python3', "updateStockProductRef.py"])#

subprocess.run(['python3', "unrollProductdetails.py"])

subprocess.run(['python3', "updatePaymentsInSales.py"])#
subprocess.run(['python3', "updateChequePaymentsInSales.py"])#

subprocess.run(['python3', "mapCreditNoteAndStockProduct.py"])#


subprocess.run(['python3', "mapReferencesSales.py"])##












