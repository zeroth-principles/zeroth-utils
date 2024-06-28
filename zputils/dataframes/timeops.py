# -*- coding: utf-8 -*-
#
# Copyright (C) 2023 Zeroth-Principles
#
# This file is part of Zeroth-Utils.
#
#  Zeroth-Utils is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Zeroth-Utils is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License along with
#  Zeroth-Utils. If not, see <http://www.gnu.org/licenses/>.

"""dataframe util file contains ops related to common time-series operations for pandas dataframe."""

__copyright__ = '2023 Zeroth Principles'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'

import pandas as pd
import logging

from zpmeta.superclasses.func import Fu


class Shift_g_Df(Fu):
    """Function class for shifting a dataframe with time-series index.
    
    Args:
        operand (DataFrame): DataFrame to be shifted.
        params (dict): parameters defining the shift.
            {
                periods (int or relativedelta): periods to shift by.
                fillna (bool): Whether to fill NaNs with the last value. Default is True.
                align (bool): Whether to align the result with the original dataframe. Default is False.
            }

    Raises:
        KeyError: _description_

    Returns:
        DataFrame: Shifted dataframe
        
    Notes:
        - The input dataframe must have a time-series index.
        
    Change Log:
        - 0.0.1: Initial commit
    """

    @classmethod
    def _std_params(cls, name: str = None) -> dict:
        return dict(periods=None, align=False, fillna=True)
     
    @classmethod        
    def _execute(cls, operand: pd.DataFrame =None, period: tuple = None, params: dict = None) -> object:
        if params['fillna']:
            content = operand.fillna(method='pad')
        else:
            content = operand.copy()

        if isinstance(params['periods'],int):
            content = content.shift(params['periods'])
        else:
            content.index = content.index.map(lambda x: x + params['periods'])            
            content = content[~content.index.duplicated(keep='last')]

        if params['align']:
            content = content.reindex(operand.index,method='pad')
        
        return content
    