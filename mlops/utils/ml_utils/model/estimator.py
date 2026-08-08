from mlops.constants.training_pipeline import model_file_name,saved_model_dir
import sys
import os
from mlops.exception.exception import customexception
from mlops.logging.logger import logging
class networkmodel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor=preprocessor
            self.model=model
        except Exception as e:
            raise customexception(e,sys)
    def predict(self,x):
        try:
            x_transform=self.preprocessor.transform(x)
            y_hat=self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise customexception(e,sys) 