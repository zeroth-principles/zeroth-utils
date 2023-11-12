"""test_timeops util file contains test cases for timeops.py file."""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']


import pandas as pd
import numpy as np
import pytest
from dateutil.relativedelta import relativedelta
from zputils.dataframes.timeops import shift_g_df


@pytest.fixture
def time_series_df():
    date_rng = pd.date_range(start='2020-01-01', end='2020-01-10', freq='D')
    df = pd.DataFrame(date_rng, columns=['date'])
    df.set_index('date', inplace=True)
    df['data'] = np.arange(0, 10)
    return df

def test_shift_g_df_positive_periods(time_series_df):
    params = {'periods': 1, 'fillna': False, 'align': False}
    expected_output = time_series_df.shift(1)
    result = shift_g_df._execute(operand=time_series_df, params=params)
    pd.testing.assert_frame_equal(result, expected_output)

def test_shift_g_df_negative_periods(time_series_df):
    params = {'periods': -1, 'fillna': False, 'align': False}
    expected_output = time_series_df.shift(-1)
    result = shift_g_df._execute(operand=time_series_df, params=params)
    pd.testing.assert_frame_equal(result, expected_output)

def test_shift_g_df_fillna(time_series_df):
    time_series_df.iloc[0, 0] = np.nan
    params = {'periods': 1, 'fillna': True, 'align': False}
    expected_output = time_series_df.fillna(method='pad').shift(1)
    result = shift_g_df._execute(operand=time_series_df, params=params)
    pd.testing.assert_frame_equal(result, expected_output)

def test_shift_g_df_align(time_series_df):
    params = {'periods': 1, 'fillna': False, 'align': True}
    expected_output = time_series_df.shift(1).reindex(time_series_df.index, method='pad')
    result = shift_g_df._execute(operand=time_series_df, params=params)
    pd.testing.assert_frame_equal(result, expected_output)

def test_shift_g_df_relativedelta(time_series_df):
    params = {'periods': relativedelta(days=1), 'fillna': False, 'align': False}
    date_rng = pd.date_range(start='2020-01-02', end='2020-01-11', freq='D')
    expected_output = pd.DataFrame(date_rng, columns=['date'])
    expected_output.set_index('date', inplace=True)
    expected_output['data'] = np.arange(0, 10)

    result = shift_g_df._execute(operand=time_series_df, params=params)
    pd.testing.assert_frame_equal(result, expected_output)
