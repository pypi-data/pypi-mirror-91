# Standard Library
import unittest

# Third party
import numpy as np
from modelbase.ode import algebraicfunctions as af


class AlgebraicFunctionTests(unittest.TestCase):
    def test_equilibrium(self):
        np.testing.assert_array_almost_equal(af.equilibrium(S=1, P=1, keq=1), (1.0, 1.0))
        np.testing.assert_array_almost_equal(af.equilibrium(S=1, P=1, keq=0), (2, 0))
        np.testing.assert_array_almost_equal(af.equilibrium(S=1, P=1, keq=1e9), (0, 2))
