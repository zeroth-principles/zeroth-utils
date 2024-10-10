"""test_dataframe util file contains test cases for dataframe util file."""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']


from zputils.dataframe import RandomReturn
import pytest
from functools import partial
import numpy as np
from pandas import date_range, MultiIndex

def test_default_distribution():
    rr = RandomReturn(params = dict(seed = 0, freq = "B", distribution = partial(np.random.normal, loc = 0.0, scale = 1.0)))
    result = rr(entities=['A', 'B'], period=('2022-01-01', '2022-01-05'))
    assert result.shape == (3, 2)  # Since freq is 'B', there will be 3 business days between the dates

def test_custom_distribution():
    custom_distribution = partial(np.random.poisson, lam = 5)
    rr = RandomReturn(params= dict(seed = 0, freq = "B", distribution= custom_distribution))
    result = rr(entities={'type': ['A', 'B'], 'sub_type': ['X', 'Y']}, period=('2022-01-01', '2022-01-05'))
    assert result.shape == (3, 4)  # 3 business days, 4 combinations of entities

def test_single_entity_str():
    rr = RandomReturn(params = dict(seed = 0, freq = "B", distribution = partial(np.random.normal, loc = 0.0, scale = 1.0)))
    result = rr(entities='A', period=('2022-01-01', '2022-01-05'))
    assert result.shape == (3, 1)

def test_invalid_distribution_dict():
    with pytest.raises(ValueError, match="distribution should be functools partial function specifying numpy method"):
        rr = RandomReturn(params=dict(seed = 0, freq = "B", distribution= np.random.normal))
        rr(entities=['A'], period=('2022-01-01', '2022-01-05'))

# def test_missing_distribution_keys():
#     with pytest.raises(ValueError, match="distribution should have func_dict and params of that func_dict defined"):
#         invalid_distribution = {"func_dict": np.random.normal}
#         rr = RandomReturn(params={"distribution": invalid_distribution})
#         rr(entities=['A'], period=('2022-01-01', '2022-01-05'))

def test_invalid_entities():
    with pytest.raises(ValueError, match="entities should be a dict, list, array or str"):
        rr = RandomReturn(params = dict(seed = 0, freq = "B", distribution = partial(np.random.normal, loc = 0.0, scale = 1.0)))
        rr(entities=123, period=('2022-01-01', '2022-01-05'))

def test_date_range_generation():
    rr = RandomReturn(params = dict(seed = 0, freq = "D", distribution = partial(np.random.normal, loc = 0.0, scale = 1.0)))
    result = rr(entities=['A'], period=('2022-01-01', '2022-01-05'))
    expected_dates = date_range('2022-01-01', '2022-01-05', freq="D")
    assert all(result.index == expected_dates)
