import os 
import sys
import mlops.exception as customexception
import pymongo
import pandas as pd
import numpy as np
from mlops.logging.logger import logging
from mlops.constants import training_pipeline_constants as tp
from mlops.entity.config_entity import dataingestionconfig
from mlops.entity.config_entity import dataingestionartifact
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()
MONGO_DB_URL=os.getenv("MONGO_db_url")
class DataIngestion:
    def __init__(self,dataingestionconfig:dataingestionconfig):
        try:
            self.dataingestionconfig=dataingestionconfig
        except Exception as e:
            raise customexception(e,sys)
    def collection_to_dataframe(self):
        try:
            database=self.dataingestionconfig.databse_name
            collectionname=self.dataingestionconfig.collection_name
            self.mongoclient=pymongo.mongo_client(MONGO_DB_URL)
            collection= self.mongoclient[database][collectionname]
            df=pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df.drop(columns=["_id"],axis=1,inplace=True)
            df.replace({"na":np.nan},inplace=True)
        except Exception as e:
            raise customexception(e,sys)
    def export_data_into_featurestore(self,dataframe:pd.DataFrame):
        try:
            featurestorefilepath=self.dataingestionconfig.feature_store_file_path
            dir_path=os.path.dirname(featurestorefilepath)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(featurestorefilepath,header=True,index=False)
            return dataframe
        except Exception as e:
            raise customexception(e,sys)
    def traintestsplit(self,dataframe:pd.DataFrame):
        try:
            train_set,test_set=train_test_split(dataframe,dataingestionconfig.train_test_split_ratio)  
            logging.info("train test split")
            dir_path=os.path.dirname(self.dataingestionconfig.train_file_name)   
            os.makedirs(dir_path,exist_ok=True)
            logging.info("export train test path")
            train_set.to_csv(self.dataingestionconfig.train_file_name,header=True,index=False)    
            test_set.to_csv(self.dataingestionconfig.test_file_name,header=True,index=False)
            logging.info("export done")
        except Exception as e:
            raise customexception(e,sys)
    def initiatedataingestion(self):
        try:
            dataframe=self.collection_to_dataframe()
            dataframe=self.export_data_into_featurestore(dataframe)
            self.traintestsplit(dataframe)
            data_ingestionartifact=dataingestionartifact(trained_file_path=self.dataingestionconfig.train_file_name,
                                                         test_file_path=self.dataingestionconfig.test_file_name)              
            return data_ingestionartifact
        except Exception as e:
            raise customexception(e,sys)

