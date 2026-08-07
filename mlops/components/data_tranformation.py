import sys
import os 
import numpy as np
import pandas as pd
from mlops.entity.artifact_entity import datavalidationartifact,dataingestionartifact,datatransformationartifact
from mlops.entity.config_entity import datavalidationconfig,datatrasformationconfig
from mlops.exception.exception import customexception
from mlops.logging.logger import logging
from mlops.utils.main_utils.utils import read_yaml_file,write_ymal_file,save_numpy_array_data,save_object
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from mlops.constants.training_pipeline import target_column
from mlops.constants.training_pipeline import data_transformation_imputer_params
from mlops.utils.main_utils.utils import save_numpy_array_data,save_object
class Datatransformation:
    def __init__(self,data_validation_arti:datavalidationartifact,data_transformation_confi:datatrasformationconfig):
        try:
            self.data_validation_artifact=data_validation_arti
            self.data_transformation_config=data_transformation_confi
        except Exception as e:
            raise customexception(e,sys)
    def read_daata(file_path)->pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise customexception(e,sys)
    def get_data_transformer_object(cls)->Pipeline:
        logging.info("get the transformer object")
        try:
            imputer:KNNImputer=KNNImputer(**data_transformation_imputer_params)
            preprocessor:Pipeline=Pipeline([("imputer",imputer)])
            return preprocessor

        except Exception as e:
            raise customexception(e,sys)
    def validate_data_tranformation(self)->datatransformationartifact:
        logging.info("data read")
        try:
            train_df=Datatransformation.read_daata(self.data_validation_artifact.valid_train_path)
            test_df=Datatransformation.read_daata(self.data_validation_artifact.valid_test_path)
            input_feature_train_df=train_df.drop(columns=[target_column],axis=1)
            target_feature_train_df=train_df[target_column]
            target_feature_train_df=target_feature_train_df.replace(-1,0)
            input_feature_test_df=test_df.drop(columns=[target_column],axis=1)
            target_feature_test_df=train_df[target_column]
            target_feature_test_df=target_feature_test_df.replace(-1,0)
            preprocessor=self.get_data_transformer_object
            preprocessor_obj=preprocessor.fit(input_feature_train_df)
            transformed_input_train=preprocessor_obj.transform(input_feature_train_df)
            transformed_input_test=preprocessor_obj.transform(input_feature_test_df)
            train_arr=np.c_(transformed_input_train,np.array(target_feature_train_df))
            test_arr=np.c_(transformed_input_test,np.array(target_feature_test_df))
            save_numpy_array_data(self.data_transformation_config.datatransformationtrainfilepath,array=train_arr)
            save_numpy_array_data(self.data_transformation_config.datatrainsformationtestfilepath,array=test_arr)
            save_object(self.data_transformation_config.datatrainformationobjectfilepath,preprocessor_obj)
            data_transformation_artifact=datatransformationartifact(
                transformed_object_file_path=self.data_transformation_config.datatrainformationobjectfilepath,
                transformed_train_file_path=self.data_transformation_config.datatransformationtrainfilepath,
                transformed_test_file_pat=self.data_transformation_config.datatrainsformationtestfilepath
            )
        except Exception as e:
            raise customexception(e,sys)    