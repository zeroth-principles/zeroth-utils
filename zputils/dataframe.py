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
from functools import partial


class RandomReturn(PanelCachedSource, metaclass=MultitonMeta):
    """
    PanelCachedSource Class for generating random returns.
    """
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
        super(RandomReturn, self).__init__(params)
        self.appendable = dict(xs=True, ts=True)
    
    def _check_consistency(self, params):
        if "distribution" not in params:
            raise ValueError("distribution should be specified")
        
        distribution  = self.params["distribution"]
        if distribution is not None:
             if not isinstance(distribution, partial):
                raise ValueError("distribution should be functools partial function specifying numpy method")
        #     if not isinstance(distribution, dict):
        #         raise ValueError("distribution should be dict")
            
        #     if "func" not in distribution and params not in distribution:
        #         raise ValueError("distribution should have func and params of that func defined")
        
    def _execute(self, call_type=None, entities=None, period=None):
        np.random.seed(self.params["seed"])
        self._check_consistency(self.params)
        if self.params["distribution"] is None:
            distribution = partial(np.random.normal, loc = 0.0, scale = 0.01)
            # distribution = dict(func = np.random.normal, params = dict(loc = 0.0, scale = 1.0))
        else:
            distribution  = self.params["distribution"]
        
        if isinstance(entities, dict):
            cols = MultiIndex.from_product([val for val in entities.values()], names=entities.keys())
        elif isinstance(entities, (list, np.ndarray)):
            cols = MultiIndex.from_product([entities], names=["entity"])
        elif isinstance(entities, str):
            cols = MultiIndex.from_product([[entities]], names=["entity"])
        elif isinstance(entities, MultiIndex):
            cols = entities
        else:
            raise ValueError("entities should be a dict, list, array or str")
        
        idx = date_range(period[0], period[1], freq=self.params['freq'])
        # values = distribution["func"](**distribution["params"], size = (len(idx), len(cols)))
        values = distribution(size = (len(idx), len(cols)))

        result = DataFrame(values, columns=cols, index=idx)
        
        return result