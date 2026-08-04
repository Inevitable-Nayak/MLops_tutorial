import os
import sys
import json
from mlops.logging.logger import logging
from dotenv import load_dotenv
load_dotenv()
mongo_db_url=os.getenv("MONGO_db_url")
import certifi
ca=certifi.where()
import pymongo
import pandas as pd
import numpy as np

import mlops.exception as customexception

class mlops_data:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise customexception(e,sys)
    def cv_to_json_convert(self,file_path):
        try:
            df=pd.read_csv(file_path)
            df.reset_index(drop=True,inplace=True)
            records=list(json.loads(df.T.to_json()).values())  
            return records
        except Exception as e:
            raise customexception(e,sys)
    def push_data_to_mongo(self,records,database,collection):
        try:
            self.records=records
            self.database=database
            self.collection=collection
            self.client=pymongo.MongoClient(mongo_db_url)  
            self.database=self.client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise customexception(e,sys)    

if __name__=="__main__":
    file_Path="C:\\Users\\nayak\\Documents\\Mlops\\MLOPS_DATA\\phisingData.csv"
    DATABASE="Amrutansu_NAyak"
    collection="ML_OPS"
    mlobj=mlops_data()
    records=mlobj.cv_to_json_convert(file_Path)
    no_of_records=mlobj.push_data_to_mongo(records,DATABASE,collection)
