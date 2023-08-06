# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
from typing import Any, Dict, List, Optional, Set, Tuple, Union

import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.utils import validation as sk_validation

from azureml._common._error_definition import AzureMLError
from azureml._common._error_definition.user_error import BadArgument
from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.core.constants import FeatureType as _FeatureType
from azureml.automl.core.constants import FeaturizationConfigMode
from azureml.automl.core.featurization import FeaturizationConfig
from azureml.automl.core.shared import constants, utilities
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    DatasetContainsInf, DataShapeMismatch, ExperimentTimeoutForDataSize, FeaturizationConfigColumnMissing,
    InvalidMetricForSingleValuedColumn, InvalidValuesInData, SampleCountMismatch, UnhashableValueInColumn,
    UnrecognizedFeatures)
from azureml.automl.core.shared.exceptions import ConfigException, DataException, ValidationException
from azureml.automl.core.shared.reference_codes import ReferenceCodes
from azureml.automl.runtime.column_purpose_detection import ColumnPurposeDetector
from azureml.automl.runtime.shared.types import DataInputType

logger = logging.getLogger(__name__)


def validate_training_data(
        X: pd.DataFrame,
        y: DataInputType,
        X_valid: Optional[pd.DataFrame],
        y_valid: Optional[DataInputType],
        sample_weight: Optional[DataInputType],
        sample_weight_valid: Optional[DataInputType],
        cv_splits_indices: Optional[List[List[Any]]],
        automl_settings: AutoMLBaseSettings,
        check_sparse: bool = False,
        x_raw_column_names: Optional[np.ndarray] = None,
) -> None:
    """
    Validate that training data and parameters have been correctly provided.

    :param X:
    :param y:
    :param X_valid:
    :param y_valid:
    :param sample_weight:
    :param sample_weight_valid:
    :param cv_splits_indices:
    :param automl_settings:
    :param check_sparse:
    :param x_raw_column_names: Raw column names as list of str.
    """
    # streaming uses subsampling + streaming does not use pandas, so the following isn't applicable - hence skip
    if automl_settings.featurization != FeaturizationConfigMode.Off and not automl_settings.enable_streaming:
        _check_data_can_be_preprocessed(X, X_valid, x_raw_column_names)

    metrics_checks(X, y, automl_settings, X_valid, y_valid)

    _validate_exp_timeout_for_data(X, automl_settings)
    _validate_featurization_config(automl_settings.featurization, x_raw_column_names)

    _validate_all_column_not_ignored(X, x_raw_column_names, automl_settings)


def check_data_nan_inf(data: DataInputType, input_data_name: str, check_nan: bool, check_inf: bool = True) -> None:
    """
    Go through each column in the data and see if they contain any nan or inf
    If nan exists in the data, we give warning
    If inf exists in the data, we throw ValueError
    :param data: data to check
    :param input_data_name: name of the data
    :param check_nan: whether to check for nan
    :param check_inf: whether to check for inf
    :return:
    """
    try:
        if check_nan:
            if _is_nan_in_data(data):
                msg = (
                    "WARNING: Input data {} contains NaN (np.NaN) data."
                    "Please review data and consider dropping the rows with NaN or turn on featurization."
                )
                print(msg.format(input_data_name))
                logger.warning(msg)

        if check_inf:
            is_inf_in_data(data, raise_exception=True, input_data_name=input_data_name)
    except DataException:
        raise
    except Exception as e:
        logger.error(
            "Failed to validate whether the input Dataset contains all finite values. " "Cannot pre-process the data."
        )
        raise DataException._with_error(
            AzureMLError.create(InvalidValuesInData, target=input_data_name), inner_exception=e
        ) from e


def _is_nan_in_data(data: DataInputType) -> bool:
    """
    Check whether data contains nan

    :param data: data to check
    :return: True if data contains nan, False otherwise
    """
    if isinstance(data, pd.DataFrame):
        return bool(pd.isna(data.values).any())
    elif sparse.issparse(data):
        return bool(pd.isna(data.data).any())
    else:
        # pd.Series and np.array
        return bool(pd.isna(data).any())


def is_inf_in_data(data: DataInputType, raise_exception: bool = False, input_data_name: str = "") -> bool:
    """
    Calls in to sklearn's assert_all_finite() implementation to check whether data contains inf.
    If a dataset failed sklearn validation, it cannot be trained by most of our pipeline.
    Reference: https://github.com/scikit-learn/scikit-learn/blob/0.19.X/sklearn/utils/validation.py)

    A ValueError is raised if the inf check fails.
    An AttributeError is raised if the input data is malformed.
    :param data: data to check
    :return: True if data contains inf, False otherwise
    """
    try:
        if isinstance(data, pd.DataFrame):
            for column in data.columns:
                sk_validation.assert_all_finite(data[column].values, allow_nan=True)
        elif isinstance(data, np.ndarray) and len(data.shape) > 1:
            for index in range(data.shape[1]):
                sk_validation.assert_all_finite(data[:, index], allow_nan=True)
        else:
            sk_validation.assert_all_finite(data, allow_nan=True)
        # if assert_all_finite did not throw, data does not contain inf, return False
        return False
    except ValueError as ve:
        # assert_all_finite throws ValueError which means data contains inf
        if raise_exception:
            raise DataException._with_error(
                AzureMLError.create(DatasetContainsInf, target=input_data_name, data_object_name=input_data_name),
                inner_exception=ve,
            )
        return True


# todo This currently exists due to data preparation dependencies on data validations (e.g., we currently do rule based
#      train/valid split - a data preparation step - before data validations, but they require X, y to be of the right
#      dimensionality, have same number of samples, etc.) - data validation step.
#      This method should be swiftly removed once we are doing data validations before data preparations.
def check_dimensions(
        X: pd.DataFrame,
        y: np.ndarray,
        X_valid: Optional[pd.DataFrame],
        y_valid: Optional[np.ndarray],
        sample_weight: Optional[np.ndarray],
        sample_weight_valid: Optional[np.ndarray],
) -> None:
    """
    Check dimensions of data inputs, by trying to create an instance of MaterializedTabularData

    :param X: Training Data
    :param y: Labels
    :param X_valid: Validation Data
    :param y_valid: Validation Labels
    :param sample_weight: Training sample weights
    :param sample_weight_valid: Validation sample weights
    :return: None
    """
    from azureml.automl.runtime._data_definition.exceptions import DataShapeException, InvalidDimensionException
    from azureml.automl.core.shared.exceptions import InvalidTypeException, InvalidValueException

    try:
        from azureml.automl.runtime._data_definition import MaterializedTabularData
        MaterializedTabularData(X, y, sample_weight)
        if X_valid is not None and y_valid is not None:
            MaterializedTabularData(X_valid, y_valid, sample_weight_valid)
    except DataShapeException as dse:
        # This is raised when X, y, weights (or X_valid, y_valid, weights_valid) have different array lengths
        raise DataException._with_error(
            AzureMLError.create(SampleCountMismatch, target=dse.target),
            inner_exception=dse
        ) from dse
    except InvalidDimensionException as ide:
        # This is raised when X, y or weights have incompatible dimensionality
        raise DataException._with_error(
            AzureMLError.create(DataShapeMismatch, target=ide.target),
            inner_exception=ide
        ) from ide
    except (InvalidValueException, InvalidTypeException) as ie:
        # This is raised when X, y, weights are null or have invalid types. (weights is optional)
        raise DataException._with_error(
            AzureMLError.create(BadArgument, argument_name=ie.target, target=ie.target),
            inner_exception=ie
        ) from ie


def _check_data_can_be_preprocessed(
        X: DataInputType, X_valid: DataInputType, x_raw_column_names: Optional[np.ndarray] = None
) -> None:
    if sparse.issparse(X):
        return
    n_x_col = 1 if len(X.shape) == 1 else X.shape[1]
    if x_raw_column_names is None and isinstance(X, np.ndarray):
        x_raw_column_names = np.arange(n_x_col)
    elif x_raw_column_names is None:
        # if pandas df, try to use columns_names from dataframe
        x_raw_column_names = X.columns

    for col_num, col_name in zip(range(n_x_col), x_raw_column_names):
        _check_column_can_be_preprocessed(_get_column_by_column_number(X, col_num), col_name, False)
        if X_valid is not None:
            _check_column_can_be_preprocessed(_get_column_by_column_number(X_valid, col_num), col_name, True)


def _check_column_can_be_preprocessed(series: pd.Series, col_name: str, is_valid_data: bool) -> None:
    try:
        # TODO: Check if this is true for all cases
        # preprocess need pandas.unique can be run properly.
        series.unique()
    except TypeError as te:
        input_type = "X_valid" if is_valid_data else "X"
        raise DataException._with_error(
            AzureMLError.create(
                UnhashableValueInColumn, target=input_type, column_name=col_name, data_object_name=input_type
            ),
            inner_exception=te,
        ) from te


def _get_column_by_column_number(X: DataInputType, col_num: int) -> pd.Series:
    if isinstance(X, np.ndarray) and len(X.shape) == 1:
        return pd.Series(X)
    elif isinstance(X, np.ndarray):
        return pd.Series(X[:, col_num])
    else:
        return pd.Series(X.iloc[:, col_num])


def metrics_checks(
        x: DataInputType,
        y: DataInputType,
        automl_settings: AutoMLBaseSettings,
        x_valid: Optional[DataInputType] = None,
        y_valid: Optional[DataInputType] = None,
) -> None:
    """
    Validate input data for metrics.

    :param x: input data. dataframe/ array/ sparse matrix
    :param y: input labels. dataframe/series/array
    :param automl_settings: automl settings
    :raise: DataException if data is not suitable for metrics calculations
    :return:
    """
    if y_valid is not None:
        # since we subsample the data for streaming following calculations may be inaccurate - hence skip them
        if automl_settings.task_type == constants.Tasks.CLASSIFICATION and not automl_settings.enable_streaming:
            primary_metric = automl_settings.primary_metric
            if primary_metric == constants.Metric.AUCWeighted:
                in_valid = set(y_valid[~pd.isnull(y_valid)])
                if len(in_valid) == 1:
                    remaining_metrics = utilities.get_primary_metrics(constants.Tasks.CLASSIFICATION).copy()
                    remaining_metrics.remove(primary_metric)
                    raise DataException._with_error(
                        AzureMLError.create(
                            InvalidMetricForSingleValuedColumn,
                            target="y_valid",
                            data_object_name="y_valid",
                            valid_primary_metrics=remaining_metrics,
                        )
                    )


def _validate_exp_timeout_for_data(X: DataInputType, automl_settings: AutoMLBaseSettings) -> None:
    if sparse.issparse(X):
        return

    if X is not None and automl_settings is not None:
        if automl_settings.experiment_timeout_minutes is not None:
            n_rows = X.shape[0]
            n_cols = 1 if len(X.shape) < 2 else X.shape[1]
            # 1M is the timeout needs to be 60 min
            if (
                    n_rows * n_cols > constants.AutoMLValidation.TIMEOUT_DATA_BOUND and
                    automl_settings.experiment_timeout_minutes < 60
            ):
                raise ValidationException._with_error(
                    AzureMLError.create(
                        ExperimentTimeoutForDataSize,
                        target="experiment_timeout_minutes",
                        minimum=60,
                        maximum="{:,}".format(constants.AutoMLValidation.TIMEOUT_DATA_BOUND),
                        rows=n_rows,
                        columns=n_cols,
                        total=n_rows * n_cols,
                        reference_code=ReferenceCodes._VALIDATE_EXP_TIMEOUT_WITH_DATA,
                    )
                )


def _validate_all_column_not_ignored(
        X: DataInputType, x_raw_column_names: Optional[np.ndarray], automl_settings: AutoMLBaseSettings
) -> None:
    """
    Validate whether all columns will be dropped by AutoML or not during featurization.

    :param X: The X input data.
    :param x_raw_column_names: A list of input x column names.
    :param automl_settings: The automl settings.
    """
    if isinstance(X, np.ndarray) or isinstance(X, pd.DataFrame):
        # todo Not sure what this is doing at this place, this should be removed
        from azureml.automl.runtime.featurizer.transformer.timeseries._validation import _get_df_or_raise
        df = _get_df_or_raise(X, x_raw_column_names, True)
    else:
        # no check for the sparse scenario
        return

    featurization = automl_settings.featurization
    is_customized_featurization_enabled = isinstance(automl_settings.featurization, dict)

    # There is no data transformation when featurization is off.
    if featurization == FeaturizationConfigMode.Off:
        return

    # Featurization auto mode, all the related column set is empty.
    customized_columns = set()  # type: Set[str]
    transformer_params_column_set = set()  # type: Set[str]
    if is_customized_featurization_enabled:
        drop_columns_set = set(featurization.get("_drop_columns") or [])  # type: ignore
        column_purpose_keep_column_dict = {}  # type: Dict[str, str]
        column_purpose_drop_column_dict = {}  # type: Dict[str, str]
        if featurization.get("_column_purposes") is not None:  # type: ignore
            for column, purpose in featurization.get("_column_purposes").items():  # type: ignore
                if purpose in _FeatureType.DROP_SET:
                    column_purpose_drop_column_dict[column] = purpose
                else:
                    column_purpose_keep_column_dict[column] = purpose

        transformer_params = featurization.get("_transformer_params") or {}  # type: ignore
        for transfom_param in transformer_params.values():
            for cols, _ in transfom_param:
                transformer_params_column_set = transformer_params_column_set.union(cols)
        featurization_keep_column_set = set(column_purpose_keep_column_dict.keys())
        featurization_drop_column_set = drop_columns_set.union(column_purpose_drop_column_dict.keys())
        customized_columns = featurization_drop_column_set.union(featurization_keep_column_set)

    stats_and_column_purposes = ColumnPurposeDetector.get_raw_stats_and_column_purposes(df)

    not_auto_dropped_columns = set()  # type: Set[str]
    column_drop_reason_list = []  # type: List[str]
    dropped_transformer_params_column = []  # type: List[Tuple[str, str]]
    for _, feature_type_detected, column in stats_and_column_purposes:
        if feature_type_detected in _FeatureType.DROP_SET and column not in customized_columns:
            column_drop_reason_list.append("Column {} identified as {}.".format(column, feature_type_detected))
            if column in transformer_params_column_set:
                dropped_transformer_params_column.append((column, feature_type_detected))
        else:
            not_auto_dropped_columns.add(column)
    # This should be logged via ConsoleInterface. Commenting this out until ConsoleInterface is available here.
    # if len(dropped_transformer_params_column) > 0:
    #     print("The following transformer_params in featurization config will be ignored as the these columns are"
    #           "automatically dropped by AutoML. If you still want to use these columns, please set correct value"
    #           "in column_purposes of featurizaiton config:")
    #     for col, purpose in dropped_transformer_params_column:
    #         print("Column {}, AutoML detected type {}.".format(col, purpose))

    if len(not_auto_dropped_columns) == 0:
        raise DataException._with_error(
            AzureMLError.create(
                UnrecognizedFeatures,
                target="X",
                column_drop_reasons="\n".join(column_drop_reason_list),
                reference_code=ReferenceCodes._VALIDATE_ALL_COLUMN_IGNORED,
            )
        )

    # Only check this part if featurization config is enabled.
    if is_customized_featurization_enabled:
        final_keep_column = set()  # type: Set[str]
        for column in sorted(not_auto_dropped_columns):
            if column not in featurization_drop_column_set:
                final_keep_column.add(column)
            if column in drop_columns_set:
                column_drop_reason_list.append(
                    "Column {}, included in featurization config's drop columns.".format(column)
                )
            if column in column_purpose_drop_column_dict:
                column_drop_reason_list.append(
                    "Column {}, marked as {} in featurization config.".format(
                        column, column_purpose_drop_column_dict[column]
                    )
                )

        if len(final_keep_column) == 0:
            raise DataException._with_error(
                AzureMLError.create(
                    UnrecognizedFeatures,
                    target="featurization_config",
                    column_drop_reasons="\n".join(column_drop_reason_list),
                    reference_code=ReferenceCodes._VALIDATE_ALL_COLUMN_IGNORED_FEATURIZATION,
                )
            )


def _validate_featurization_config(
        featurization: Union[str, Dict[str, Any]], x_raw_column_name: Optional[np.ndarray]
) -> None:
    """
    Check if columns with custom purpose or featurization are present in the column list.

    :param featurization: The featurization config object.
    :param x_raw_column_name: the data frame column names.
    :raises: ConfigException
    """
    if x_raw_column_name is None:
        return
    if isinstance(featurization, FeaturizationConfig):
        if featurization.column_purposes is not None:
            for col in featurization.column_purposes.keys():
                if col not in x_raw_column_name:
                    raise ConfigException._with_error(
                        AzureMLError.create(
                            FeaturizationConfigColumnMissing,
                            target="X",
                            columns=col,
                            sub_config_name="column_purposes",
                            all_columns=x_raw_column_name,
                            reference_code=ReferenceCodes._VALIDATE_FEATURIZATION_PURPOSE_TIMESERIES,
                        )
                    )
        if featurization.transformer_params is not None:
            for _, col_param_list in featurization.transformer_params.items():
                for col_param in col_param_list:
                    if col_param[0] not in x_raw_column_name:
                        raise ConfigException._with_error(
                            AzureMLError.create(
                                FeaturizationConfigColumnMissing,
                                target="X",
                                columns=col_param[0],
                                sub_config_name="transformer_params",
                                all_columns=x_raw_column_name,
                                reference_code=ReferenceCodes._VALIDATE_FEATURIZATION_TRANSFORM_TIMESERIES,
                            )
                        )
