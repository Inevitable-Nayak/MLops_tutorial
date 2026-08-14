import sys
import numpy as np
import pandas as pd

from mlops.entity.artifact_entity import (
    datavalidationartifact,
    datatransformationartifact
)

from mlops.entity.config_entity import datatrasformationconfig

from mlops.exception.exception import customexception
from mlops.logging.logger import logging

from mlops.utils.main_utils.utils import (
    save_numpy_array_data,
    save_object
)

from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from mlops.constants.training_pipeline import (
    target_column,
    data_transformation_imputer_params
)


class Datatransformation:

    def __init__(
        self,
        datavalidationartifact: datavalidationartifact,
        data_transformation_config: datatrasformationconfig
    ):

        try:

            self.data_validation_artifact = datavalidationartifact
            self.data_transformation_config = data_transformation_config

        except Exception as e:
            raise customexception(e, sys)

    def read_daata(self, file_path):

        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise customexception(e, sys)

    def get_data_transformer_object(self):

        try:

            imputer = KNNImputer(
                **data_transformation_imputer_params
            )

            preprocessor = Pipeline([
                ("imputer", imputer)
            ])

            return preprocessor

        except Exception as e:
            raise customexception(e, sys)

    def validate_data_tranformation(self):

        try:

            train_df = self.read_daata(
                self.data_validation_artifact.valid_train_path
            )

            test_df = self.read_daata(
                self.data_validation_artifact.valid_test_path
            )

            input_feature_train_df = train_df.drop(
                columns=[target_column]
            )

            target_feature_train_df = train_df[
                target_column
            ]

            input_feature_test_df = test_df.drop(
                columns=[target_column]
            )

            target_feature_test_df = test_df[
                target_column
            ]

            target_feature_train_df = (
                target_feature_train_df.replace(-1, 0)
            )

            target_feature_test_df = (
                target_feature_test_df.replace(-1, 0)
            )

            preprocessor = (
                self.get_data_transformer_object()
            )

            preprocessor_obj = preprocessor.fit(
                input_feature_train_df
            )

            transformed_input_train = (
                preprocessor_obj.transform(
                    input_feature_train_df
                )
            )

            transformed_input_test = (
                preprocessor_obj.transform(
                    input_feature_test_df
                )
            )

            train_arr = np.c_[
                transformed_input_train,
                np.array(target_feature_train_df)
            ]

            test_arr = np.c_[
                transformed_input_test,
                np.array(target_feature_test_df)
            ]

            save_numpy_array_data(
                self.data_transformation_config.datatransformationtrainfilepath,
                array=train_arr
            )

            save_numpy_array_data(
                self.data_transformation_config.datatrainsformationtestfilepath,
                array=test_arr
            )

            save_object(
                self.data_transformation_config.datatrainformationobjectfilepath,
                preprocessor_obj
            )

            return datatransformationartifact(
                transformed_object_file_path=self.data_transformation_config.datatrainformationobjectfilepath,
                transformed_train_file_path=self.data_transformation_config.datatransformationtrainfilepath,
                transformed_test_file_path=self.data_transformation_config.datatrainsformationtestfilepath
            )

        except Exception as e:
            raise customexception(e, sys)