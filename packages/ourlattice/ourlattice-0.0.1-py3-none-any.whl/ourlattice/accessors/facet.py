import pandas as pd
import numpy as np

from ourlattice.accessors.lattice import Lattice, SupportFieldType

@pd.api.extensions.register_series_accessor("facet")
class Facet(Lattice):
    
    def __init__(self, pandas_obj):
        super(Facet, self).__init__(pandas_obj)
        
    @staticmethod
    def _validate(obj):
        should_be_in_index = [
            SupportFieldType.B.value,
        ]
        if not np.isin(should_be_in_index, obj.index).all():
            raise AttributeError(f"Must have {should_be_in_index} indexes in series.")

    @property
    def variables(self):
        return self._obj.index[self._obj.index != SupportFieldType.B.value]