# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
import warnings
from typing import Optional, Union, Tuple, cast

import numpy as np
import pandas as pd
from scipy import sparse

from azureml._common._error_definition import AzureMLError
from azureml._common._error_definition.user_error import BadArgument
from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.core.constants import FeaturizationConfigMode
from azureml.automl.core.shared import logging_utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    DatasetsFeatureCountMismatch,
    DataShapeMismatch,
    InsufficientSampleSize,
    MissingValidationConfig,
    NCrossValidationsExceedsTrainingRows,
    NonOverlappingColumnsInTrainValid,
    SampleCountMismatch,
)
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.core.shared._diagnostics.validation import Validation
from azureml.automl.core.shared.exceptions import (
    DataException,
    InvalidTypeException,
    InvalidValueException,
    ValidationException,
)
from azureml.automl.runtime._data_definition import MaterializedTabularData, RawExperimentData
from azureml.automl.runtime._data_definition.exceptions import DataShapeException, InvalidDimensionException
from azureml.automl.runtime._ml_engine.validation import common_data_validations
from azureml.automl.runtime._ml_engine.validation.validators import AbstractRawExperimentDataValidator

from .materialized_tabular_data_validator import MaterializedTabularDataValidator

logger = logging.getLogger(__name__)


class RawExperimentDataValidator(AbstractRawExperimentDataValidator):
    """
    Run all necessary data validations on the experiment data, to make sure we can produce a machine learning
    model on it.
    """

    def __init__(self, automl_settings: AutoMLBaseSettings, check_sparse: bool) -> None:
        """
        Initialize a RawExperimentDataValidator

        :param automl_settings: The settings for the experiment.
        :param check_sparse: If validations on sparse data should also be done.
        """
        self._automl_settings = automl_settings
        self._check_sparse = check_sparse

    def validate(self, raw_experiment_data: RawExperimentData) -> None:
        """
        Run validations on the user provided data inputs (such as training and validation datasets)

        :param raw_experiment_data: The data to validate.
        :return: None, raises an exception if validation fails.
        """
        Contract.assert_value(raw_experiment_data, "raw_experiment_data")
        Contract.assert_type(raw_experiment_data, "raw_experiment_data", expected_types=RawExperimentData)

        try:
            self.validate_raw_experiment_data(raw_experiment_data)
        except (DataException, ValidationException):
            raise
        except Exception as e:
            logging_utilities.log_traceback(e, logger)
            new_exception = ValidationException.from_exception(e, target="RawExperimentDataValidation")
            raise new_exception.with_traceback(e.__traceback__)

    def validate_raw_experiment_data(self, raw_experiment_data: RawExperimentData) -> None:
        """
        Given raw experiment data, check if it is valid to run through the featurization and model training pipelines

        :param raw_experiment_data: RawExperimentData, as provided by the user
        :return: None
        :raises: DataException, ValidationException
        """
        # Validate that required values are provided, and are of the right types
        self._validate_basic(raw_experiment_data)

        # Ensure at least one form of validation is specified
        self._check_validation_data_or_config_provided(raw_experiment_data)

        # Get the training and validation tabular datasets
        train_data, validation_data = self._get_train_valid_data(raw_experiment_data)

        self._check_data_minimal_size(train_data.X, validation_data.X if validation_data else None)

        tabular_data_validator = self._get_tabular_data_validator()     # type: MaterializedTabularDataValidator

        # The rest of validations on training dataset happen separately
        tabular_data_validator.validate(train_data)

        if validation_data is not None:
            # Run rest of the validations plus any validations *across* train-valid datasets
            tabular_data_validator.validate(validation_data)

            # The rest of the train valid validations happen in this function
            self.validate_train_valid_data(train_data, validation_data)

        # todo port the validations in the following call into the above hierarchy
        self._validate_old_style(raw_experiment_data)

    def validate_train_valid_data(
        self, train_data: MaterializedTabularData, validation_data: MaterializedTabularData
    ) -> None:
        """
        Validate data across training and validation datasets.

        :param train_data: The data to train the model on.
        :param validation_data: The data to validate the predictability of the model against.
        :return:
        """
        X = train_data.X
        X_valid = validation_data.X

        Contract.assert_true(type(X) == type(X_valid), "X & X_valid are of different types.", log_safe=True)

        self._check_train_valid_data_has_same_columns(X, X_valid)
        self._check_train_valid_dimensions(X, X_valid)

    def _validate_old_style(self, raw_experiment_data: RawExperimentData) -> None:
        X = raw_experiment_data.X
        y = raw_experiment_data.y
        sample_weight = raw_experiment_data.weights

        X_valid = raw_experiment_data.X_valid
        y_valid = raw_experiment_data.y_valid
        sample_weight_valid = raw_experiment_data.weights_valid

        cv_splits_indices = raw_experiment_data.cv_splits_indices
        x_raw_column_names = raw_experiment_data.feature_column_names

        common_data_validations.validate_training_data(
            X,
            y,
            X_valid,
            y_valid,
            sample_weight,
            sample_weight_valid,
            cv_splits_indices,
            self._automl_settings,
            self._check_sparse,
            cast(np.ndarray, x_raw_column_names),
        )

        # todo To be moved out into it's own timeseries specific validator
        if self._automl_settings.is_timeseries:
            from azureml.automl.runtime import _time_series_training_utilities

            _time_series_training_utilities.validate_timeseries_training_data(
                self._automl_settings,
                X,
                y,
                X_valid,
                y_valid,
                sample_weight,
                sample_weight_valid,
                cv_splits_indices,
                cast(np.ndarray, x_raw_column_names),
            )

    def _get_tabular_data_validator(self) -> MaterializedTabularDataValidator:
        """Create an appropriate tabular data validator given the configuration."""
        is_timeseries = self._automl_settings.is_timeseries
        is_featurization_turned_on = self._automl_settings.featurization != FeaturizationConfigMode.Off
        is_featurization_required = is_timeseries or is_featurization_turned_on
        tabular_data_validator = MaterializedTabularDataValidator(
            task_type=self._automl_settings.task_type,
            primary_metric=self._automl_settings.primary_metric,
            is_onnx_enabled=self._automl_settings.enable_onnx_compatible_models,
            is_featurization_required=is_featurization_required,
            is_streaming_enabled=self._automl_settings.enable_streaming,
        )
        return tabular_data_validator

    def _check_train_valid_data_has_same_columns(
        self, X: Union[pd.DataFrame, sparse.spmatrix], X_valid: Union[pd.DataFrame, sparse.spmatrix]
    ) -> None:
        """Validate if training and validation datasets have the same columns."""
        if isinstance(X, pd.DataFrame):
            if len(X.columns.intersection(X_valid.columns)) != len(X.columns):
                x_column_list = list(X.columns)
                x_valid_column_list = list(X_valid.columns)
                missing_columns = set([col for col in x_column_list if x_valid_column_list.count(col) == 0])
                raise DataException(
                    azureml_error=AzureMLError.create(
                        NonOverlappingColumnsInTrainValid, target="X", missing_columns=", ".join(missing_columns)
                    )
                )

    def _check_train_valid_dimensions(
        self, X: Union[pd.DataFrame, sparse.spmatrix], X_valid: Union[pd.DataFrame, sparse.spmatrix]
    ) -> None:
        # todo not sure what does this validation actually checks?
        if len(X.shape) > 1:
            if len(X_valid.shape) > 1 and X.shape[1] != X_valid.shape[1]:
                raise DataException(
                    azureml_error=AzureMLError.create(
                        DatasetsFeatureCountMismatch,
                        target="X/X_Valid",
                        first_dataset_name="X",
                        first_dataset_shape=X.shape[1],
                        second_dataset_name="X_valid",
                        second_dataset_shape=X_valid.shape[1],
                    )
                )
            elif len(X_valid.shape) == 1 and X.shape[1] != 1:
                raise DataException(
                    azureml_error=AzureMLError.create(
                        DatasetsFeatureCountMismatch,
                        target="X/X_Valid",
                        first_dataset_name="X",
                        first_dataset_shape=X.shape[1],
                        second_dataset_name="X_valid",
                        second_dataset_shape=1,
                    )
                )
        elif len(X_valid.shape) > 1 and X_valid.shape[1] != 1:
            raise DataException(
                azureml_error=AzureMLError.create(
                    DatasetsFeatureCountMismatch,
                    target="X/X_Valid",
                    first_dataset_name="X",
                    first_dataset_shape=X.shape[1],
                    second_dataset_name="X_valid",
                    second_dataset_shape=X_valid.shape[1],
                )
            )

    def _check_data_minimal_size(
        self, X: Union[pd.DataFrame, sparse.spmatrix], X_valid: Optional[Union[pd.DataFrame, sparse.spmatrix]]
    ) -> None:
        """Validate whether the training and validation datasets have a desired minimum number of samples."""
        number_of_training_rows = X.shape[0]
        if self._automl_settings.n_cross_validations is not None:
            if number_of_training_rows < self._automl_settings.n_cross_validations:
                raise DataException(
                    azureml_error=AzureMLError.create(
                        NCrossValidationsExceedsTrainingRows,
                        target="n_cross_validations",
                        training_rows=number_of_training_rows,
                        n_cross_validations=self._automl_settings.n_cross_validations,
                    )
                )
        # todo this shouldn't take an 'if_timeseries' flag, timeseries validator needs to override this method
        if not self._automl_settings.is_timeseries:
            if number_of_training_rows < SmallDataSetLimit.MINIMAL_TRAIN_SIZE:
                raise DataException(
                    azureml_error=AzureMLError.create(
                        InsufficientSampleSize,
                        target="X",
                        data_object_name="X",
                        sample_count=number_of_training_rows,
                        minimum_count=SmallDataSetLimit.MINIMAL_TRAIN_SIZE,
                    )
                )
            if X_valid is not None and X_valid.shape[0] < SmallDataSetLimit.MINIMAL_VALIDATION_SIZE:
                raise DataException(
                    azureml_error=AzureMLError.create(
                        InsufficientSampleSize,
                        target="X_valid",
                        data_object_name="X_valid",
                        sample_count=X_valid.shape[0],
                        minimum_count=SmallDataSetLimit.MINIMAL_VALIDATION_SIZE,
                    )
                )
            if number_of_training_rows < SmallDataSetLimit.WARNING_SIZE:
                warnings.warn(
                    "The input data X has {} data points which is less than the recommended "
                    "minimum data size {}. Please consider adding more data points to ensure better model "
                    "accuracy.".format(number_of_training_rows, SmallDataSetLimit.WARNING_SIZE)
                )

    # todo This should eventually move up to configuration validation
    def _check_validation_data_or_config_provided(self, raw_experiment_data: RawExperimentData) -> None:
        """
        Validate if user provided any dataset or configuration which can later be used to run validations on a model.
        """
        from azureml.automl.core.config_utilities import _check_validation_config

        is_validation_dataset_provided = raw_experiment_data.X_valid is not None
        is_cv_folds_provided = raw_experiment_data.n_cross_validations
        is_cv_indices_provided = raw_experiment_data.cv_splits_indices is not None
        is_validation_size_config_provided = raw_experiment_data.validation_size != 0
        if not (
                is_validation_dataset_provided or is_cv_folds_provided or
                is_cv_indices_provided or is_validation_size_config_provided
        ):
            raise DataException(
                azureml_error=AzureMLError.create(
                    MissingValidationConfig,
                    target=", ".join(["validation_data", "validation_size", "n_cross_validations"]),
                )
            )

        _check_validation_config(
            X_valid=raw_experiment_data.X_valid,
            y_valid=raw_experiment_data.y_valid,
            sample_weight=raw_experiment_data.weights,
            sample_weight_valid=raw_experiment_data.weights_valid,
            cv_splits_indices=raw_experiment_data.cv_splits_indices,
            n_cross_validations=raw_experiment_data.n_cross_validations,
            validation_size=raw_experiment_data.validation_size,
        )

    def _validate_basic(self, raw_experiment_data: RawExperimentData) -> None:
        """
        Ensure that:
            - X, y are non-null
            - X, y & weights are of the right types
            - If X_valid is provided, y_valid must also be provided
            - X_valid, y_valid and weights_valid are of the right types
        """
        # training data checks
        Validation.validate_value(raw_experiment_data.X, "X")
        Validation.validate_value(raw_experiment_data.y, "y")
        # supported types for 'X'
        if not sparse.issparse(raw_experiment_data.X):
            Validation.validate_type(raw_experiment_data.X, "X", (pd.DataFrame, np.ndarray))
        # supported types for 'y'
        Validation.validate_type(raw_experiment_data.y, "y", np.ndarray)
        if raw_experiment_data.weights is not None:
            Validation.validate_type(raw_experiment_data.weights, "sample_weight", expected_types=np.ndarray)

        # validation data checks
        if raw_experiment_data.X_valid is not None:
            Validation.validate_type(raw_experiment_data.X_valid, "X_valid", (pd.DataFrame, np.ndarray))
            Validation.validate_value(raw_experiment_data.y_valid, "y_valid")
            Validation.validate_type(raw_experiment_data.y_valid, "y_valid", np.ndarray)
            if raw_experiment_data.weights is not None:
                Validation.validate_value(raw_experiment_data.weights_valid, "weights_valid")
                Validation.validate_type(raw_experiment_data.weights_valid, "weights_valid", expected_types=np.ndarray)

    def _get_train_valid_data(
        self, raw_experiment_data: RawExperimentData
    ) -> Tuple[MaterializedTabularData, Optional[MaterializedTabularData]]:
        """
        Return the training/validation dataset pair from raw experiment data.

        This does not **currently split** the data, it will simply return any validation data if it was
        present in the data dictionary with which this class was initialized (i.e. if the user provided one)

        :return: training and validation tabular datasets
        :raises InvalidValueException, InvalidTypeException, DataShapeException, InvalidDimensionException
        """
        train_data = None  # type: Optional[MaterializedTabularData]
        valid_data = None  # type: Optional[MaterializedTabularData]

        try:
            # Attempt to create train and valid tabular datasets. Any discrepancies in the data will be raised
            # as exceptions, which is wrapped as user errors and re-thrown
            train_data = MaterializedTabularData(
                raw_experiment_data.X, raw_experiment_data.y, raw_experiment_data.weights
            )

            if raw_experiment_data.X_valid is not None and raw_experiment_data.y_valid is not None:
                valid_data = MaterializedTabularData(
                    raw_experiment_data.X_valid, raw_experiment_data.y_valid, raw_experiment_data.weights_valid
                )
        except DataShapeException as dse:
            # This is raised when X, y, weights (or X_valid, y_valid, weights_valid) have different array lengths
            raise DataException(
                azureml_error=AzureMLError.create(SampleCountMismatch, target=dse.target), inner_exception=dse
            ) from dse
        except InvalidDimensionException as ide:
            # This is raised when X, y or weights have incompatible dimensionality
            raise DataException(
                azureml_error=AzureMLError.create(DataShapeMismatch, target=ide.target), inner_exception=ide
            ) from ide
        except (InvalidValueException, InvalidTypeException) as ie:
            # This is raised when X, y, weights are null or have invalid types. (weights is optional)
            raise DataException(
                azureml_error=AzureMLError.create(BadArgument, argument_name=ie.target, target=ie.target),
                inner_exception=ie,
            ) from ie

        return train_data, valid_data


class SmallDataSetLimit:
    """Constants for the small dataset limit."""

    WARNING_SIZE = 100
    MINIMAL_TRAIN_SIZE = 50
    MINIMAL_VALIDATION_SIZE = int(MINIMAL_TRAIN_SIZE / 10)
