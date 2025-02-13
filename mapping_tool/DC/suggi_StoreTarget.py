from pymongo import MongoClient
from tqdm import tqdm
import pandas as pd
from load_config import load_config
config = load_config()
from IPython import embed

import calendar
import datetime

client = MongoClient("mongodb://localhost:27017")  
db = client[config['target']]
target_db = client[config["target"]]

excel_file_path = './store_data/Target Distribution.xlsx'
df = pd.read_excel(excel_file_path)
rows_as_dicts = df.to_dict(orient='records')

MM = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec"
}

for row in rows_as_dicts:
    try:
        TM = row["TM"]
        Store = row["Store"]
        Category = row["Category"]
        print("running for ", Store , "for category" , Category )
        for key in row.keys():
            if key in ["TM","Store","Category"]:
                continue
            else:
                days_in_month=calendar.monthrange(key.year, key.month)[1]
                for day in range(1,days_in_month+1):
                    data={}
                    data['Store']=Store
                    data['TM']=TM
                    data['Category']=Category
                    data['Month']=MM[key.month]
                    data['Year']=key.year
                    data['Date']=datetime.datetime(key.year,key.month,day)
                    data['Daily_Target']=(row[key]*100000)/days_in_month
                    data['Target']=row[key]*100000
                    target_db.Store_Target.insert_one(data)
                
    except Exception as error:
        print(error)


    

    