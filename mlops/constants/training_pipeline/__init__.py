import os
import sys
from datetime import datetime
import pandas as pd
import numpy as np

target_column="Result"
pipeline_name="mlops"   
artifacts_dir="artifacts"
file_name="phisingData.csv"
train_file_name="train.csv"
test_file_name="test.csv"
data_ingestion_collection_name="ML_OPS"
data_ingestion_database_name="Amrutansu_NAyak"
data_ingested_dir_name="data_ingestion"
data_ingestion_feature_store_dir="feature_store"
data_ingestion_ingested_dir="ingested"
data_ingestion_train_test_split_ratio=0.2
data_validation_dirname:str="datavaalidation"
data_validation_valid_dir:str="validdata"
data_validation_invalid_data:str="invaliddata"
data_validation_drift_report_dir:str="drift_repport"
data_validation_drfit_report_filename:str="report.yaml"
schema_file_path="schema.yaml"
PREPROCESSING_OBJECT_FILE_NAME = "preprocessing.pkl"
data_transformation_dir_name:str="data_transformation"
data_transformation_transformed_data_dir:str="transformed"
data_transformation_transformed_object_dir:str="transsformed_obj"
data_transformation_imputer_params:dict={
    "missing_values":np.nan,
    "n_neighbours":3,
    "weights":"uniform",
}

