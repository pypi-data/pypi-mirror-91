# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Classe for TimeseriesColumnNameValidationWorker."""
from typing import Set

from azureml._common._error_definition import AzureMLError
from azureml.automl.core.shared._diagnostics.automl_error_definitions import (
    TimeseriesCannotDropSpecialColumn, TimeseriesTimeColNameOverlapIdColNames)
from azureml.automl.core.shared.forecasting_exception import ForecastingConfigException
from azureml.automl.core.shared.logging_utilities import function_debug_log_wrapped
from azureml.automl.core.shared.reference_codes import ReferenceCodes

from ._timeseries_validator import TimeseriesValidationParamName
from ._timeseries_validator import TimeseriesValidationParameter
from ._timeseries_validator import TimeseriesValidationWorkerBase


class TimeseriesColumnNameValidationWorker(TimeseriesValidationWorkerBase):
    """Validation worker for the column names."""

    def __init__(self) -> None:
        pass

    @function_debug_log_wrapped('info')
    def validate(self, param: TimeseriesValidationParameter) -> None:
        """Abstract method that validate the timeseries config/data."""
        automl_settings = param.params[TimeseriesValidationParamName.AUTOML_SETTINGS]
        if automl_settings.grain_column_names is None:
            grain_set = set()  # type: Set[str]
        else:
            grain_set = set(automl_settings.grain_column_names)

        # Set the grain set for later validation workers.
        param.params[TimeseriesValidationParamName.GRAIN_SET] = grain_set

        # Validate the drop column names.
        if automl_settings.drop_column_names is not None:
            drop_set = set(automl_settings.drop_column_names)
            if (automl_settings.time_column_name in drop_set):
                raise ForecastingConfigException._with_error(
                    AzureMLError.create(TimeseriesCannotDropSpecialColumn,
                                        target='automl_settings.drop_column_names',
                                        reference_code=ReferenceCodes._TS_CANNOT_DROP_SPECIAL_COL_TM,
                                        column_name='Time')
                )
            # Check if grain columns are overlapped with drop columns.
            if automl_settings.grain_column_names is not None:
                if drop_set.intersection(grain_set):
                    raise ForecastingConfigException._with_error(
                        AzureMLError.create(TimeseriesCannotDropSpecialColumn,
                                            target='automl_settings.drop_column_names',
                                            reference_code=ReferenceCodes._TS_CANNOT_DROP_SPECIAL_COL_TM_IDX,
                                            column_name='Time series identifier')
                    )

        # Validate the time column name.
        if automl_settings.time_column_name in grain_set:
            raise ForecastingConfigException._with_error(
                AzureMLError.create(TimeseriesTimeColNameOverlapIdColNames, target='time_series_id_values',
                                    reference_code=ReferenceCodes._TS_TIME_COL_NAME_OVERLAP_ID_COL_NAMES,
                                    time_column_name=automl_settings.time_column_name)
            )
