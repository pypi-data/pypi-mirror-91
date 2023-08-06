"""
Unittests for spacing_functions module
"""


import unittest
import numpy as np
from binarycpython.utils.spacing_functions import *


class test_spacing_functions(unittest.TestCase):
    """
    Unit test for spacing functions
    """

    def test_const(self):
        """
        Unittest for function const
        """

        const_return = const(1, 10, 10)
        self.assertTrue(
            (const_return == np.linspace(1, 10, 10)).all(),
            msg="Output didn't contain SINGLE_STAR_LIFETIME",
        )
