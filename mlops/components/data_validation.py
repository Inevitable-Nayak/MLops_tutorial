from mlops.entity.artifact_entity import datavalidationartifact,dataingestionartifact
from mlops.entity.config_entity import datavalidationconfig
from mlops.exception.exception import customexception
from mlops.logging.logger import logging
from mlops.utils.main_utils.utils import read_yaml_file,write_ymal_file
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import os
import sys
from mlops.constants.training_pipeline import schema_file_path
class Datavalidation:
    def __init__(self,data_ingestion_arti:dataingestionartifact,data_validation_confi=datavalidationconfig):
        try:
            self.data_ingestion_artifact=self.data_ingestion_arti
            self.data_ingestion_config=data_validation_confi
            self._schema_config=read_yaml_file(schema_file_path)
        except Exception as e:
            raise customexception(e,sys)    
    def read_data(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise customexception(e,sys)
    def validate_coloumns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_coloumns=len(self._schema_config)
            logging.info("compare")
            if dataframe.columns == number_of_coloumns:
                return True
            return False
        except Exception as e:
            raise customexception (e,sys)
    def detect_drift(self,base_df,current_df,threshold=0.05)->bool:
        try:
            status=True
            report={}
            for column in base_df:
                d1=base_df[column]
                d2=current_df[column]
                is_same=ks_2samp(d1,d2)
                if threshold<=is_same.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{
                    "p_value":float(is_same.pvalue),
                    "drift_status":is_found

                }}

                )
            drift_report_file_path=self.datavalidationconfig.drift_report_file_path
            dir_name=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_name,exist_ok=True)
            read_yaml_file(file_path=drift_report_file_path,content=report)        

        except Exception as e:
            raise customexception(e,sys)    

            
    def initiate_data_validation(self)->datavalidationartifact:
        train_file_path=self.data_ingestion_artifact.trained_file_path
        test_file_path=self.data_ingestion_artifact.test_file_path
        train_dataframe=Datavalidation.read_data(train_file_path)
        test_dataframe=Datavalidation.read_data(test_file_path)
        status= self.validate_coloumns(dataframe=train_dataframe)
        if not status:
            error_message="very bAad"
        status= self.validate_coloumns(dataframe=test_dataframe)
        if not status:
            error_message="verryyyyyyyyyyyyyy baaaaaaaaaaaaaaad"
        status=self.detect_drift(base_df=train_dataframe,current_df=test_dataframe)
        dir_path=os.path.dirname(self.datavalidationconfig.valid_train_path)
        os.makedirs(dir_path,exist_ok=True)
        train_dataframe.to_csv(self.datavalidationconfig.valid_train_path,index=False,header=True)
        test_dataframe.to_csv(self.datavalidationconfig.valid_test_path,index=False,header=True)
        data_validatio_artifact=datavalidationartifact(
            validation_status=status,
            valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
            valid_test_file_path=self.data_ingestion_artifact.test_file_path,
            invalid_train_file_path=None,
            invalid_test_file_path=None,
            drift_report_file_path=self.data_validation_config.drift_report_file_path,
        )