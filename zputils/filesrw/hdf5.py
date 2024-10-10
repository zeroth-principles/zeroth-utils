# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 Zeroth-Principles.
# 
# Created on 7/29/2024 by Zeroth-Principles-Engineering.
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

from zpmeta.funcs.func import Func
import pandas as pd
import numpy as np
import tables as tb


class HDF5_g_DoDf(Func):
    @classmethod
    def _std_params(cls, name=None):
        params = dict(fpath=None, gpath='/', mode='w')
        return params

    @classmethod
    def _execute(cls, operand=None, params: dict = None) -> None:
        try:
            file = tb.open_file(params['fpath'], mode=params['mode'])
        except FileNotFoundError:
            raise IOError(f"File not found: {params['fpath']}")
        else:
            with file:
                for key, df in operand.items():
                    table_path = params['gpath'] + "/" + key

                    # Check if the table exists in the file
                    if file.__contains__(table_path):
                        if params['mode'] == 'w':
                            file.remove_node(table_path, recursive=True)
                            description = np.dtype([(name, df[name].dtype) for name in df.columns])
                            table = file.create_table(where=params['gpath'], name=key, description=description, title=key, createparents=True)
                        else:
                            table = file.get_node(table_path)
                    else:
                        description = np.dtype([(name, df[name].dtype) for name in df.columns])
                        table = file.create_table(where=params['gpath'], name=key, description=description, title=key, createparents=True)

                    # Reorder DataFrame columns to match the table's column order
                    column_order = table.colnames
                    df = df[column_order]

                    # Convert DataFrame to a record array
                    record_array = df.to_records(index=False)

                    # Append data to the existing table
                    table.append(record_array)
                    table.flush()

        return None


class Query_g_HDF5(Func):
    @classmethod
    def _std_params(cls, name=None):
        params = dict(fpath=None, gpath='/', mode='r')
        return params

    @classmethod
    def _execute(cls, operand=None, params: dict = None) -> None:
        try:
            file = tb.open_file(params['fpath'])
        except FileNotFoundError:
            raise IOError(f"File not found: {params['fpath']}")
        else:
            with file:
                results = {}
                for key in operand:
                    # Check if the table exists in the file
                    table_path = params['gpath'] + "/" + key
                    if file.__contains__(table_path):
                        table = file.get_node(table_path)
                        recs = table.read_where(operand[key])
                        results[key] = pd.DataFrame.from_records(recs)
                    else:
                        raise KeyError(f"Path not found: {table_path}")

        return results


if __name__ == '__main__':
    data1 = {'A': [1, 2, 3], 'B': [4, 5, 6]}
    data2 = {'C': [7, 8, 9], 'D': [10, 11, 12]}
    data3 = {'E': [13, 14, 15], 'F': [16, 17, 18]}

    df1 = pd.DataFrame(data1)
    df2 = pd.DataFrame(data2)
    df3 = pd.DataFrame(data3)

    # # Save to HDF5
    # hdf5_writer = HDF5_g_DoDf(dict(fpath="dataframe10.h5", gpath='/group1', mode='a'))
    # hdf5_writer({'df1': df1, 'df2': df2})
    # hdf5_writer({'df3': df3}, dict(gpath='/group2'))

    # Read from HDF5
    hdf5_reader = Query_g_HDF5(dict(fpath="dataframe10.h5", gpath='/group1'))
    print(hdf5_reader({'/df1': 'A > 1', '/df2': 'C >= 8'}))




