from zpmeta.superclasses.source import Su
from zpmeta.metaclasses.singletons import MultitonMeta

import pandas as pd
import numpy as np


class SimulatedDataFrame(Su, metaclass=MultitonMeta):
    '''Subclasses Su to create a dataframe of random numbers.
    Accepts a dictionary of parameters, including:
    cols: list of column names
    '''
    def __init__(self, params: dict = None):
        super(SimulatedDataFrame, self).__init__(params)
        self.appendable = dict(xs=True, ts=True)
    
    def _execute(self, call_type=None, entities=None, period=None):
        cols = pd.MultiIndex.from_product([val for val in entities.values()], names=entities.keys())
        idx = pd.date_range(period[0], period[1], freq=self.params['freq'])
        result = pd.DataFrame(np.random.randn(len(idx), len(cols)), columns=cols, index=idx)
        
        return result
    
