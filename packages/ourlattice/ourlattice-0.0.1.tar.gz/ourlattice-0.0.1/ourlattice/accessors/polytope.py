import hashlib
import pandas as pd
import numpy as np

from ourlattice.accessors.lattice import Lattice, SupportFieldType
from ourlattice.accessors.facet import Facet
from ourlattice.utils.storages.storage import Storage

from typing import Callable, List, Dict

@pd.api.extensions.register_dataframe_accessor("polytope")
class Polytope(Lattice):

    support_value_index = {
        SupportFieldType.ID: 0,
        SupportFieldType.R: 1,
        SupportFieldType.W: 2,
    }
    
    def __init__(self, pandas_obj):
        super(Polytope, self).__init__(
            obj=pandas_obj,
        )

    @staticmethod
    def construct(id: str, constraints: List[Dict[str, int]]) -> pd.DataFrame:

        """
            Groups ID and R values into indices for frame.

            Return: Polytope / pd.DataFrame
        """

        try:
            polytope = pd.DataFrame(constraints).set_index([
                SupportFieldType.ID.value, 
                SupportFieldType.R.value,
                SupportFieldType.W.value,
            ]).sort_index()
            polytope.id = id
            polytope.hash = None
        except Exception as e:
            raise Exception(f"Could not construct polytope from constraints because of error: {e}")

        return polytope

    @staticmethod
    def _validate(obj):
        # verify there is all support fields are in object
        should_be_in_columns = [
            SupportFieldType.B.value,
        ]
        if not np.isin(should_be_in_columns, obj.columns).all():
            raise AttributeError(f"Must have {should_be_in_columns} columns in frame.")
        
        should_be_in_index = [
            SupportFieldType.R.value,
            SupportFieldType.ID.value,
            SupportFieldType.W.value,
        ]
        if not np.isin(should_be_in_index, obj.index.names).all():
            raise AttributeError(f"Must have {should_be_in_index} indexes in frame.")
            
    @property
    def variables(self):
        msk = ~np.isin(self._obj.columns, [
            SupportFieldType.B.value,
        ])
        return self._obj.columns[msk]
            
    @property
    def A(self) -> pd.DataFrame:
        return self._obj.loc[:, self.variables]
    
    @property
    def b(self) -> pd.Series:
        return self._obj[SupportFieldType.B.value]
    
    @property
    def w(self) -> pd.Series:
        return self._index_row(support_field_type=SupportFieldType.W)

    @property
    def r(self) -> pd.Series:
        return self._index_row(support_field_type=SupportFieldType.R)
    
    @property
    def id(self) -> pd.Series:
        return self._index_row(support_field_type=SupportFieldType.ID)

    def _index_row(self, support_field_type: SupportFieldType) -> pd.Series:
        r = np.array([list(k) for k in self._obj.index.values])[:, self.support_value_index[support_field_type]]
        return pd.Series(r)


    def strip(self):
        """
            Removes variables/columns with only zero as constant. 
        """
        A = self.A.loc[:, (self.A != 0).any(axis=0)]
        A[SupportFieldType.B.value] = self.b
        return A
            
    def is_valid(self, x: pd.Series)-> bool:
        return (self.A.dot(x) >= self.b).all()
    
    def to_constraints(self):
        return [
            {
                **{
                    SupportFieldType.ID.value: i[0],
                    SupportFieldType.R.value: i[1],
                    SupportFieldType.W.value: i[2],
                }, 
                **r[r != 0].to_dict()
            } 
            for i, r in self._obj.iterrows()
        ]
    
    # def to_dimacscnf(self, handlers: Dict[str, Callable[[pd.Series], List[Expression]]]):

    #     """
    #         Converts into a DIMACS CNF.

    #         Return: tuple(dict, DimacsCNF)
    #     """

    #     exprs_kv = {}
    #     for (_id, rule, _), row in self._obj.iterrows():
    #         if not _id in exprs_kv:
    #             fn = handlers.get(rule, None)
    #             if not fn:
    #                 raise NotImplementedError(f"Missing handler for rule type '{rule}'")
                
    #             exprs_kv[_id] = fn(row)

    #     exprs = list(exprs_kv.values())
    #     result = expr2dimacscnf(
    #         And(*exprs).tseitin(),
    #     )

    #     return result

    # def number_of_solutions(self, sharp_sat_solver: Callable[[DimacsCNF], int], handlers: Dict[str, Callable[[pd.Series], List[Expression]]]):

    #     """
    #         Calculates the number of solutions n in this polytope.

    #         Args:
    #             sharp_sat_solver: (DimacsCNF) -> (int)
    #         Return: int
    #     """

    #     _, cnf_file_format = self.to_dimacscnf(handlers=handlers)
    #     n = sharp_sat_solver(cnf_file_format)
    #     return n

    async def save(self, _id: str, storage: Storage, compress="gzip"):
        await storage.upload_data(
            _id=_id,
            obj=self._obj,
            meta={
                "id": _id,
                "hash": self.generate_hash(),
            },
            compress=compress,
        )

    @staticmethod    
    async def load(self, _id: str, storage: Storage, decompress="gzip"):
        df = await storage.download_data(
            _id=_id,
            decompress=decompress,
        )
        return df

    def generate_hash(self) -> str:
        df = self._obj
        ignore_column_names = [
            SupportFieldType.R.value,
            SupportFieldType.B.value,
            SupportFieldType.ID.value,
        ]
        columns_sorted = sorted(list(df.columns))
        variable_header_sorted = [name for name in columns_sorted if name not in ignore_column_names]
        bts_columns = ''.join(variable_header_sorted).encode('utf-8')

        values = df[columns_sorted].values.astype(np.int16)
        indices_sorted = np.argsort([str(row) for row in values])
        bts_values = values[indices_sorted].tobytes()

        bts_box = b''.join((bts_columns, bts_values))

        return hashlib.sha256(bts_box).hexdigest()

    def errors(self, point: pd.Series) -> pd.DataFrame:
        """
            Finding what facets that are not satisfied from given config.

            Args:
                combination: pd.Series

            Return: 
                Polytope / pd.DataFrame
        """
        errors_df = self._obj[self.A.dot(point) < self.b]
        errors_df = errors_df.polytope.strip()

        return errors_df