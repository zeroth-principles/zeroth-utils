"""test_subsetting util file contains test cases for subsetting file."""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']


from zputils.dataframes.subsetting import subset_g_df
import pytest
from functools import partial
import numpy as np
import pandas as pd


@pytest.fixture
def sample_df():
    data = {
        ('A', 'x'): [1, 4, 7],
        ('A', 'y'): [2, 5, 8],
        ('B', 'x'): [3, 6, 9],
    }
    df = pd.DataFrame(data)
    df.columns.names = ['letters', 'coordinates']
    return df

def test_subset_g_df_valid_input(sample_df):
    params = {
        'by': {'letters': ['A']},
        'axis': 'columns',
        'drop_level': False,
        'find_all': True,
    }
    expected_output = sample_df.iloc[:, :2]
    result = subset_g_df._execute(operand=sample_df, params=params)
    pd.testing.assert_frame_equal(result, expected_output)

def test_subset_g_df_level_not_found(sample_df):
    params = {
        'by': {'non_existent_level': ['A']},
        'axis': 'columns',
        'drop_level': False,
        'find_all': True,
    }
    with pytest.raises(KeyError, match="Level non_existent_level not found in the dataframe"):
        subset_g_df._execute(operand=sample_df, params=params)

def test_subset_g_df_find_all_false(sample_df):
    params = {
        'by': {'non_existent_level': ['A']},
        'axis': 'columns',
        'drop_level': False,
        'find_all': False,
    }
    # Assuming that your function should return the original dataframe
    # if find_all is False and the level is not found
    expected_output = sample_df
    result = subset_g_df._execute(operand=sample_df, params=params)
    pd.testing.assert_frame_equal(result, expected_output)