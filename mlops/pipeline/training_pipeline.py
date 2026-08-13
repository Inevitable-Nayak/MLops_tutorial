import os
import sys
import numpy as np
import pandas as pd
from mlops.components.data_ingestion import DataIngestion
from mlops.components.data_validation import Datavalidation
from mlops.components.data_tranformation import Datatransformation
from mlops.components.model_trainer import modeltrainer
from mlops.logging.logger import logging
from mlops.exception.exception import customexception
from mlops.entity.config_entity import (
    trainingpipelineconfig,
    dataingestionconfig,
    datatrasformationconfig,datavalidationconfig,modeltrainerconfig
)
from mlops.entity.artifact_entity import(
    dataingestionartifact,datatransformationartifact,datavalidationartifact,modeltrainerartifact
)
class trainingpipeline:
    def __init__(self):
        self.training_pipeLine_config=trainingpipelineconfig()
    def startdataingestion(self):
        try:
            self.dataingestionconfig=dataingestionconfig(trainingpipelineconfig=self.training_pipeLine_config)
            logging.info("datata ingestion startted")
            data_ingestion=DataIngestion(dataingestion=self.dataingestionconfig)
            dataingestionartifact=data_ingestion.initiatedataingestion()
            logging.info("completed data ingestion")
            return dataingestionartifact
        except Exception as e:
            raise customexception(e,sys)
    def startdatavalidation(self,da_ingestion_artifact:dataingestionartifact):
        try:
            self.data_validation_config=datavalidationconfig(trainingpipelineconfig=self.training_pipeLine_config)
            logging.info("data validation started")
            data_validation=Datavalidation(data_ingestion_arti=da_ingestion_artifact,data_validation_confi=self.data_validation_config)
            data_validationartifact=data_validation.initiate_data_validation()
            logging.info("data_validationartifact completed")
            return data_validationartifact
        except Exception as e:
            raise customexception(e,sys)
            
    def startdatatransformation(self,datavalidationartifact:datavalidationartifact):
        try:
            self.datatransformationconfig=datatrasformationconfig(trainingpipelineconfig=self.training_pipeLine_config)
            data_transformation=Datatransformation(datavalidationartifact=datavalidationartifact,data_transformation_config=self.datatransformationconfig)
            data_transformation_artifact=data_transformation.validate_data_tranformation()
            logging.info("data tranformation complted")
            return data_transformation_artifact
        except Exception as e:
            raise customexception(e,sys)
    def startmodeltrainer(self,datatransformationartifact:datatransformationartifact):
        try:
            self.modeltrainerconfig=modeltrainerconfig(trainingpipelineconfig=self.training_pipeLine_config)
            model_trainer=modeltrainer(data_transformation_artifact=datatransformationartifact,model_trainer_config=modeltrainerconfig)
            modeltrainerartifact=model_trainer.initiate_model_trainer()
            logging.info("model tainer config completeed")
            return modeltrainerartifact
        except Exception as e:
            raise customexception (e,sys)    
    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.startdataingestion()

            data_validation_artifact=self.startdatavalidation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artiifact=self.startdatavalidation(datavalidationartifact=data_validation_artifact)
            model_trainer_artifact=self.startmodeltrainer(datatransformationartifact=data_transformation_artiifact)
            return model_trainer_artifact
        except Exception as e:
            raise customexception(e,sys)
