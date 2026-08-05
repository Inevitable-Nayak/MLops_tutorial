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