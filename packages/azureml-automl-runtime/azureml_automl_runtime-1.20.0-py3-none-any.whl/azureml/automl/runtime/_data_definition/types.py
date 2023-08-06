# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
from typing import TypeVar

import pandas as pd

import azureml.dataprep as dprep

DataFrameLike = TypeVar("DataFrameLike", pd.DataFrame, dprep.Dataflow)
