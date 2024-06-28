# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Zeroth-Principles.
# 
# Created on 1/28/2024 by Zeroth-Principles-Engineering.
# For suggestions, please write to engineering@zeroth-principles.com.
#
#  Zeroth-Meta is free software: you can redistribute it and/or modify it under the
#  terms of the GNU General Public License as published by the Free Software
#  Foundation, either version 3 of the License, or (at your option) any later
#  version.
#
#  Zeroth-Meta is distributed in the hope that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR
#  A PARTICULAR PURPOSE. See the GNU General Public License for more details.
#  You should have received a copy of the GNU General Public License along with
#  Zeroth-Meta. If not, see <http://www.gnu.org/licenses/>.

__copyright__ = '2024 Zeroth Principles'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = []

""" * """
import pandas as pd
import logging

from zpmeta.funcs.func import Func


class Df_g_DoDf(Func):
    """Function class for joining a dictionary of dataframe

    Args:
        operand (dict): DataFrame.
        params (dict): parameters defining the subset.
            {
                by (dict): Dictionary of level names as keys and level values as values.
                axis (str): Axis to subset on. Default is 'columns'.
                drop_level (bool): Whether to drop the levels that are subsetted on. Default is False.
                find_all (bool): Whether to raise and error if all the levels in the dictionary are not found. Default is True.
            }

    Raises:
        KeyError: _description_

    Returns:
        DataFrame: Subsetted dataframe

    Notes:
        - The input dataframe must have a names attribute on whatever axis is being subsetted.

    TODO:
        - need to implement for rows as well

    Change Log:
        - 0.0.1: Initial commit
    """

    @classmethod
    def _std_params(cls, name: str = None) -> dict:
        return dict(by=None, axis='columns', drop_level=False)

    @classmethod
    def _execute(cls, operand: pd.DataFrame = None, params: dict = None) -> object:
        joined_df = pd.concat(operand, axis=params['axis'], join='outer', sort=True)

        if params['drop_level']:
            joined_df = joined_df.droplevel(level=params['axis'])

        return joined

