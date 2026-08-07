from datetime import datetime
import os,sys
from mlops.constants import training_pipeline as tp
print(tp.target_column)

print(tp.data_ingestion_collection_name)
class trainingpipelineconfig:
    def __init__(self,timestamp=datetime.now()):
        self.pipeline_name=tp.pipeline_name
        self.artifacts_name=tp.artifacts_dir
        self.timestamp=datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        self.timestamp=timestamp
        self.artifacts_dir=os.path.join(self.artifacts_name,self.timestamp)
class dataingestionconfig:
    def __init__(self,training_pipeline:trainingpipelineconfig):
        self.data_ingestion_dir:str=os.path.join(
            training_pipeline.artifacts_name,tp.data_ingestion_dir_name
        )
        self.feature_store_file_path:str=os.path.join(self.data_ingestion_dir,tp.data_ingestion_feature_store_dir,tp.file_name)
        self.ingested_train_file_path:str=os.path.join(self.data_ingestion_dir,tp.data_ingestion_ingested_dir,tp.train_file_name)
        self.ingested_test_file_path:str=os.path.join(self.data_ingestion_dir,tp.data_ingestion_ingested_dir,tp.test_file_name)
        self.collection_name:str=tp.data_ingestion_collection_name
        self.train_test_split_ratio:float=tp.data_ingestion_train_test_split_ratio
        self.databse_name:str=tp.data_ingestion_database_name

class datavalidationconfig:
    def __init__(self,train_pipe:trainingpipelineconfig):
        self.datavalidationdir:str=os.path.join(trainingpipelineconfig.artifact_dir,tp.data_validation_dirname)
        self.valid_data_dir:str=os.path.join(self.datavalidationdir,tp.data_validation_valid_dir)
        self.invalid_data_dir:str=os.path.join(self.datavalidationdir,tp.data_validation_invalid_data)
        self.valid_train_path:str=os.path.join(self.datavalidationdir,tp.train_file_name)
        self.valid_test_path:str=os.path.join(self.datavalidationdir,tp.test_file_name)
        self.invalid_train_path:str=os.path.join(self.datavalidationdir,tp.train_file_name)
        self.invalid_test_path:str=os.path.join(self.datavalidationdir,tp.test_file_name)
        self.drift_report_file_path:str=os.path.join(self.datavalidationdir,tp.data_validation_drift_report_dir,tp.data_validation_drfit_report_filename)

class datatrasformationconfig:
    def __init__(self,train_pipe:trainingpipelineconfig):
        self.datatransformationdir:str=os.path.join(trainingpipelineconfig.artifact_dir,tp.data_transformation_dir_name)
        self.datatransformationtrainfilepath:str=os.path.join(self.datatransformationdir,tp.data_transformation_transformed_data_dir,tp.train_file_name.replace("csv","npy"))
        self.datatrainsformationtestfilepath:str=os.path.join(self.datatransformationdir,tp.data_transformation_transformed_data_dir,tp.test_file_name.replace("csv","npy"))
        self.datatrainformationobjectfilepath:str=os.path.join(self.datatransformationdir,tp.data_transformation_transformed_object_dir,tp.PREPROCESSING_OBJECT_FILE_NAME)
         

    