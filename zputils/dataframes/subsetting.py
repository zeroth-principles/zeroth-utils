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

"""dataframe util file contains ops related to common functions for pandas dataframe."""

__copyright__ = '2023 Zeroth Principles'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']

import pandas as pd
import logging

from zpmeta.funcs.func import Func

class subset_g_df(Func):
    """Function class for subsetting a dataframe based on a dictionary of level names as keys 
    and level values as values.
    
    Args:
        operand (DataFrame): DataFrame to be subsetted.
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
        return dict(by=None, axis='columns', drop_level=False, find_all=True)
     
    @classmethod        
    def _execute(cls, operand: pd.DataFrame =None, period: tuple = None, params: dict = None) -> object:
        # TODO: Currently Implemented for columns only, n
        
        # convert the MultiIndex columns of the operand to a DataFrame
        attributes = pd.DataFrame(operand.columns.tolist(), columns = operand.columns.names)
        
        for key, value in params['by'].items():
            try:
                attributes = attributes.loc[attributes[key].isin(value)==True]
            except KeyError as e:
                if params['find_all']:
                    raise KeyError("Level {} not found in the dataframe".format(key))
        
        cols = pd.MultiIndex.from_frame(attributes)
        result = operand[cols]
                
        return result
    
