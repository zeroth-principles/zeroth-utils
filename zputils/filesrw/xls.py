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
#

"""Code to read/write from/to XLS files."""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'


from zpmeta.funcs.func import Func
import pandas as pd


class XLS_g_DoDf(Func):
    """File writer for XLS files.

    Args:
        operand (Dict of DataFrame): Dict of DataFrames to be written to XLS.
        params (dict): parameters for writing the file
            {
                fpath (str): Path to write the file to.
                format (str): Format of the file. Default is 'xlsx'.
            }

    Raises:
        IOError: File not found error

    Returns:
        None: None
        
    Notes:
        - The labels will be written as sheet names.
        
    Examples:
        - examples\eg_filesrw.ipynb
        
    TODO:
        - If sheet names are too long, they will be truncated.
        - If sheet names are not unique, they will be made unique.
        
    Change Log:
        - 0.0.1: Initial commit
    """
    @classmethod
    def _std_params(cls, name=None):
        params = dict(fpath=None, format='xlsx', if_sheet_exists=None)
        return params

    @classmethod
    def _execute(cls, operand=None, params: dict = None) -> None:
        # check if operand is a DataFrame
        if isinstance(operand, pd.DataFrame):
            operand = dict(Sheet1=operand)
            
        if params['format'] in ['xls', 'xlsx']:
            with pd.ExcelWriter(f"{params['fpath'][0]}\{params['fpath'][1]}.{params['format']}", 
                                engine='xlsxwriter', if_sheet_exists=params['if_sheet_exists']) as writer:
                for label, label_df in operand.items():
                    if label_df is not None:
                        label_df.to_excel(writer, sheet_name=f"{label}", index=True)
       
        return None


class DoDf_g_XLS(Func):
    """Read XLS file data into a dictionary of dataframes.
    """
    @classmethod
    def _std_params(cls, name=None):
        params = dict(folder=None, sheet_names=None, index_col=None, header=None, parse_dates=True)
        return params

    @classmethod
    def _execute(cls, operand=None, params: dict = None): #-> Dict[str, pd.DataFrame]:
        if params['folder'] is None:
            fpath = operand
        else:
            fpath = params['folder']+"\\"+operand

        results = dict()
        with pd.ExcelFile(fpath) as reader:
            for sheet in reader.sheet_names:
                results[sheet] = pd.read_excel(reader, sheet_name=sheet, index_col=params['index_col'], header=params['header'],
                                               parse_dates=params['parse_dates'])

        return results
