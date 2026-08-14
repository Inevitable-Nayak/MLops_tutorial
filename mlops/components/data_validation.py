import sys

from mlops.entity.artifact_entity import (
    datavalidationartifact,
    dataingestionartifact
)

from mlops.entity.config_entity import datavalidationconfig

from mlops.exception.exception import customexception
from mlops.logging.logger import logging

from mlops.utils.main_utils.utils import (
    read_yaml_file,
    write_ymal_file
)

import pandas as pd
import os

from scipy.stats import ks_2samp

from mlops.constants.training_pipeline import schema_file_path


class Datavalidation:

    def __init__(
        self,
        data_ingestion_arti: dataingestionartifact,
        data_validation_confi: datavalidationconfig
    ):

        try:

            self.data_ingestion_artifact = data_ingestion_arti
            self.data_validation_config = data_validation_confi

            self._schema_config = read_yaml_file(
                schema_file_path
            )

        except Exception as e:
            raise customexception(e, sys)

    def read_data(self, file_path):

        try:
            return pd.read_csv(file_path)

        except Exception as e:
            raise customexception(e, sys)

    def validate_columns(self, dataframe):

        try:

            expected_columns = len(
                self._schema_config
            )

            actual_columns = len(
                dataframe.columns
            )

            return actual_columns == expected_columns

        except Exception as e:
            raise customexception(e, sys)

    def detect_drift(
        self,
        base_df,
        current_df,
        threshold=0.05
    ):

        try:

            status = True
            report = {}

            for column in base_df.columns:

                d1 = base_df[column]
                d2 = current_df[column]

                is_same = ks_2samp(d1, d2)

                drift_found = is_same.pvalue < threshold

                if drift_found:
                    status = False

                report[column] = {
                    "p_value": float(is_same.pvalue),
                    "drift_status": drift_found
                }

            drift_report_file_path = (
                self.data_validation_config.drift_report_file_path
            )

            write_ymal_file(
                file_path=drift_report_file_path,
                content=report
            )

            return status

        except Exception as e:
            raise customexception(e, sys)

    def initiate_data_validation(self):

        try:

            train_file_path = (
                self.data_ingestion_artifact.trained_file_path
            )

            test_file_path = (
                self.data_ingestion_artifact.test_file_path
            )

            train_dataframe = self.read_data(
                train_file_path
            )

            test_dataframe = self.read_data(
                test_file_path
            )

            train_status = self.validate_columns(
                train_dataframe
            )

            test_status = self.validate_columns(
                test_dataframe
            )

            drift_status = self.detect_drift(
                train_dataframe,
                test_dataframe
            )

            status = (
                train_status
                and test_status
                and drift_status
            )

            os.makedirs(
                os.path.dirname(
                    self.data_validation_config.valid_train_path
                ),
                exist_ok=True
            )

            train_dataframe.to_csv(
                self.data_validation_config.valid_train_path,
                index=False
            )

            test_dataframe.to_csv(
                self.data_validation_config.valid_test_path,
                index=False
            )

            return datavalidationartifact(
                validationstatus=status,
                valid_train_path=self.data_validation_config.valid_train_path,
                invalid_train_path=None,
                valid_test_path=self.data_validation_config.valid_test_path,
                invalid_test_path=None,
                drift_report_path=self.data_validation_config.drift_report_file_path
            )

        except Exception as e:
            raise customexception(e, sys)