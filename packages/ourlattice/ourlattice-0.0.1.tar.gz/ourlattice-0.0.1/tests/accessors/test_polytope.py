import pandas as pd
import numpy as np

from unittest import TestCase
from ourlattice.accessors.lattice import SupportFieldType
from ourlattice.accessors.polytope import Polytope

class TestPolytope(TestCase):

    def helper_get_valid_df(self):

        cnsts = [
            {
                "a": 1, 
                "b": 1, 
                "c": 1, 
                SupportFieldType.B.value: 1, 
                SupportFieldType.R.value: "exactly_one",
                SupportFieldType.ID.value: 0,    
                SupportFieldType.W.value: 10,
            },
            {
                "a": -1, 
                "b": -1, 
                "c": -1, 
                SupportFieldType.B.value: -1, 
                SupportFieldType.R.value: "exactly_one",
                SupportFieldType.ID.value: 0,    
                SupportFieldType.W.value: 10,
            },
        ]

        df = Polytope.construct(
            id="test-id",
            constraints=cnsts,
        )
        return df


    def test_will_fail_with_attribute_error_when_invalid_constraints(self):

        cnstss = [
            [
                {
                    "a":1, "b":1,
                }
            ],
            [
                {
                    "a":1, "b":1, "#id": 1,
                }
            ],
            [
                {
                    "a":1, "b":1, "#id": 1, "#r": "m"
                }
            ],
        ]

        for cnsts in cnstss:
            df = pd.DataFrame(cnsts)
            self.assertRaises(AttributeError, Polytope._validate, df)

    def test_can_fetch_r(self):

        df = self.helper_get_valid_df()
        _ = df.polytope.r

    def test_can_fetch_id(self):

        df = self.helper_get_valid_df()
        _ = df.polytope.id

    def test_can_fetch_w(self):

        df = self.helper_get_valid_df()
        _ = df.polytope.w

    def test_can_strip_polytope(self):

        df = self.helper_get_valid_df()
        df.loc[:, 'M'] = np.zeros((df.shape[0]))

        try:
            _ = df.polytope.strip()
        except Exception as e:
            self.fail(f"test_can_strip_polytope failed: {e}")

    def test_can_hash_polytope(self):

        df = self.helper_get_valid_df()
        try:
            _ = df.polytope.generate_hash()
        except Exception as e:
            self.fail(f"test_can_hash_polytope failed: {e}")
    
    def test_will_generate_errors_from_combination(self):

        df = self.helper_get_valid_df()
        combination = pd.Series({"a": 1, "b": 1}, index=df.polytope.variables).fillna(0)
        errors = df.polytope.errors(combination)
        self.assertGreater(errors.shape[0], 0)

    def test_will_convert_to_constraints(self):
        
        df = self.helper_get_valid_df()
        try:
            _ = df.polytope.to_constraints()
        except Exception as e:
            self.fail(f"test_will_convert_to_constraints failed: {e}")