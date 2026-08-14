from datetime import datetime
import os
from mlops.constants import training_pipeline as tp


class trainingpipelineconfig:

    def __init__(self):
        self.pipeline_name = tp.pipeline_name
        self.artifacts_name = tp.artifacts_dir
        self.timestamp = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

        self.artifacts_dir = os.path.join(
            self.artifacts_name,
            self.timestamp
        )


class dataingestionconfig:

    def __init__(self, trainingpipelineconfig: trainingpipelineconfig):

        self.data_ingestion_dir = os.path.join(
            trainingpipelineconfig.artifacts_dir,
            tp.data_ingestion_dir_name
        )

        self.feature_store_file_path = os.path.join(
            self.data_ingestion_dir,
            tp.data_ingestion_feature_store_dir,
            tp.file_name
        )

        self.train_file_name = os.path.join(
            self.data_ingestion_dir,
            tp.data_ingestion_ingested_dir,
            tp.train_file_name
        )

        self.test_file_name = os.path.join(
            self.data_ingestion_dir,
            tp.data_ingestion_ingested_dir,
            tp.test_file_name
        )

        self.collection_name = tp.data_ingestion_collection_name
        self.train_test_split_ratio = tp.data_ingestion_train_test_split_ratio
        self.databse_name = tp.data_ingestion_database_name


class datavalidationconfig:

    def __init__(self, trainingpipelineconfig: trainingpipelineconfig):

        self.datavalidationdir = os.path.join(
            trainingpipelineconfig.artifacts_dir,
            tp.data_validation_dirname
        )

        self.valid_data_dir = os.path.join(
            self.datavalidationdir,
            tp.data_validation_valid_dir
        )

        self.invalid_data_dir = os.path.join(
            self.datavalidationdir,
            tp.data_validation_invalid_data
        )

        self.valid_train_path = os.path.join(
            self.valid_data_dir,
            tp.train_file_name
        )

        self.valid_test_path = os.path.join(
            self.valid_data_dir,
            tp.test_file_name
        )

        self.invalid_train_path = os.path.join(
            self.invalid_data_dir,
            tp.train_file_name
        )

        self.invalid_test_path = os.path.join(
            self.invalid_data_dir,
            tp.test_file_name
        )

        self.drift_report_file_path = os.path.join(
            self.datavalidationdir,
            tp.data_validation_drift_report_dir,
            tp.data_validation_drfit_report_filename
        )


class datatrasformationconfig:

    def __init__(self, trainingpipelineconfig: trainingpipelineconfig):

        self.datatransformationdir = os.path.join(
            trainingpipelineconfig.artifacts_dir,
            tp.data_transformation_dir_name
        )

        self.datatransformationtrainfilepath = os.path.join(
            self.datatransformationdir,
            tp.data_transformation_transformed_data_dir,
            tp.train_file_name.replace("csv", "npy")
        )

        self.datatrainsformationtestfilepath = os.path.join(
            self.datatransformationdir,
            tp.data_transformation_transformed_data_dir,
            tp.test_file_name.replace("csv", "npy")
        )

        self.datatrainformationobjectfilepath = os.path.join(
            self.datatransformationdir,
            tp.data_transformation_transformed_object_dir,
            tp.PREPROCESSING_OBJECT_FILE_NAME
        )


class modeltrainerconfig:

    def __init__(self, trainingpipelineconfig: trainingpipelineconfig):

        self.modeltrainerdirname = os.path.join(
            trainingpipelineconfig.artifacts_dir,
            tp.model_trainer_dir_name
        )

        self.trainedmodelfilepath = os.path.join(
            self.modeltrainerdirname,
            tp.model_trainer_trained_model_dir,
            tp.model_trainer_trained_model_name
        )

        self.expectedaccuracy = tp.model_trainer_expected_score
        self.threshold = tp.model_trainer_threshold