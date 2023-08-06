# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from abc import ABC, abstractmethod

from azureml.automl.runtime._data_definition import RawExperimentData, MaterializedTabularData


class AbstractRawExperimentDataValidator(ABC):
    """
    Interface for data validations on the user provided RawExperimentData, across different task types.

    The different types refers to the different shapes and sizes that a machine learning
    dataset can come in, such as columns or tabular data, and for different task types such as
    Classification, Regression, Forecasting.
    """

    @abstractmethod
    def validate(self, raw_experiment_data: RawExperimentData) -> None:
        """
        Run validations on the raw experiment data.

        :param raw_experiment_data: Data to run validations on.
        :return: None
        """
        raise NotImplementedError


class AbstractTabularDataValidator(ABC):
    """
    Interface for data validations on a TabularData.
    """

    @abstractmethod
    def validate(self, tabular_data: MaterializedTabularData) -> None:
        """
        Run validations on the provided inputs.

        :param tabular_data: Data to run validations on.
        :return: None
        """
        raise NotImplementedError
