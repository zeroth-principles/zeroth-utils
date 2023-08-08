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
#  Zeroth-Quant. If not, see <http://www.gnu.org/licenses/>.f


"""dataframe util file contains ops related to common functions for pandas dataframe."""

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']

import pandas as pd
from zpmeta.superclasses.panelcachedsource import PanelCachedSource
from zpmeta.superclasses.functionclass import FunctionClass
from zpmeta.metaclasses.singletons import MultitonMeta
from pandas import DataFrame, Series, concat, MultiIndex, date_range, IndexSlice
import numpy as np
from datetime import datetime
import logging



class RandomReturn(PanelCachedSource, metaclass=MultitonMeta):
    """
    PanelCachedSource Class for generating random returns.
    """
    def __init__(self, params: dict = dict(seed = 0, freq = "B", low = -0.05, high =0.05)):
        """
        Standard parameters for the function class.
        params: dict
            seed: int
                The seed for the random number generator.
            freq: str
                The frequency of the output weights.
            low: float
                The lower bound of the random number generator.
            high: float
                The upper bound of the random number generator.
        """
        super(RandomReturn, self).__init__(params)
        self.appendable = dict(xs=True, ts=True)
    
    def execute(self, call_type=None, entities=None, period=None):
        cols = MultiIndex.from_product([val for val in entities.values()], names=entities.keys())
        idx = date_range(period[0], period[1], freq=self.params['freq'])
        result = DataFrame(np.random.Generator.uniform(low = self.params["low"], high = self.params["high"],
                                                       size = (len(idx), len(cols))), columns=cols, index=idx)
        
        return result