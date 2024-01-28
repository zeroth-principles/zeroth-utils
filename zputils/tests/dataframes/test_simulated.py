"""test_simulated util file contains test cases for simulated.py file."""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']


from zputils.dataframes.simulated import SimulatedDataFrame
import pytest
from functools import partial
import numpy as np
from pandas import date_range

def test_default_distribution():
    rr = SimulatedDataFrame(params = dict(seed = 0, freq = "B", distribution = partial(np.random.normal, loc = 0.0, scale = 0.05)))
    result = rr(entities=['A', 'B'], period=('2022-01-01', '2022-01-05'))
    assert result.shape == (3, 2)  # Since freq is 'B', there will be 3 business days between the dates

def test_custom_distribution():
    custom_distribution = partial(np.random.poisson, lam = 5)
    rr = SimulatedDataFrame(params= dict(seed = 0, freq = "B", distribution= custom_distribution))
    result = rr(entities={'type': ['A', 'B'], 'sub_type': ['X', 'Y']}, period=('2022-01-01', '2022-01-05'))
    assert result.shape == (3, 4)  # 3 business days, 4 combinations of entities



def test_date_range_generation():
    rr = SimulatedDataFrame(params = dict(seed = 0, freq = "D", distribution = partial(np.random.normal, loc = 0.0, scale = 0.05)))
    result = rr(entities=['A'], period=('2022-01-01', '2022-01-05'))
    expected_dates = date_range('2022-01-01', '2022-01-05', freq="D")
    assert all(result.index == expected_dates)
