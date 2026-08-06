from mlops.entity.artifact_entity import datavalidationartifact
from mlops.entity.config_entity import datavalidationconfig
from mlops.exception.exception import customexception
from mlops.logging.logger import logging
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp
import os
import sys
from mlops.constants.training_pipeline import schema_file_path
class Datavalidation:
    def __init__(self,data_ingestion_arti:datavalidationartifact,data_ingestion_confi=datavalidationconfig):
        try:
            self.data_ingestion_artifact=data_ingestion_arti
            self.data_ingestion_config=data_ingestion_confi
            self._schema_config=read_ymal_file(schema_file_path)