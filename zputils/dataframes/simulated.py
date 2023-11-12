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

__copyright__ = '2023 Zeroth Principles Research'
__license__ = 'GPLv3'
__docformat__ = 'google'
__author__ = 'Zeroth Principles Engineering'
__email__ = 'engineering@zeroth-principles.com'
__authors__ = ['Deepak Singh <deepaksingh@zeroth-principles.com>']


import pandas as pd
import numpy as np
from zpmeta.sources.panelsource import PanelSource
from zpmeta.singletons.singletons import MultitonMeta
from pandas import DataFrame, Series, concat, MultiIndex, date_range, IndexSlice
import numpy as np
from datetime import datetime
import logging
from functools import partial

class SimulatedDataFrame(PanelSource, metaclass=MultitonMeta):
    '''Subclasses PanelCachedSource to create a dataframe of random numbers.
    Accepts a dictionary of parameters, including:
    cols: list of column names
    '''
    def __init__(self, params: dict = dict(seed = 0, freq = "B", distribution = None)):
        """
        Standard parameters for the function class.
        params: dict
            seed: int
                The seed for the random number generator.
            freq: str
                The frequency of the output weights.
            distribution: callable
                Numpy distribution function wrapped in functools partial, default is standard normal distribution.
        """
        super(SimulatedDataFrame, self).__init__(params)
        self.appendable = dict(xs=True, ts=True)
        self._check_consistency()

    @staticmethod
    def _check_consistency(params):
        if "distribution" not in params:
            raise ValueError("distribution should be specified")
        
        distribution  = params["distribution"]
        if distribution is not None:
             if not isinstance(distribution, partial):
                raise ValueError("distribution should be functools partial function specifying numpy method")
             
    def _execute(self, entities=None, period=None):
        np.random.seed(self.params["seed"])
        if self.params["distribution"] is None:
            distribution = partial(np.random.normal, loc = 0.0, scale = 0.01)
            # distribution = dict(func = np.random.normal, params = dict(loc = 0.0, scale = 1.0))
        else:
            distribution  = self.params["distribution"]
        
        if isinstance(entities, dict):
            cols = MultiIndex.from_product([val for val in entities.values()], names=entities.keys())
        # elif isinstance(entities, (list, np.ndarray)):
        #     cols = MultiIndex.from_product([entities], names=["entity"])
        # elif isinstance(entities, str):
        #     cols = MultiIndex.from_product([[entities]], names=["entity"])
        # elif isinstance(entities, MultiIndex):
        #     cols = entities
        else:
            cols = entities
            # raise ValueError("entities should be a dict, list, array or str")
        
        idx = date_range(period[0], period[1], freq=self.params['freq'])
        # values = distribution["func"](**distribution["params"], size = (len(idx), len(cols)))
        values = distribution(size = (len(idx), len(cols)))

        result = DataFrame(values, columns=cols, index=idx)
                
        return result
    

