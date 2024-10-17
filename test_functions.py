import unittest
import numpy as np
from helper import calcRSAMvalue_withoutNumpy

# RSAM calculation:
# calculate offet and substract it from all the values in the array
# take the absolut values from this and then build the mean again
#
# exists to check against the selfwritten functions which dont use numpy
#
def calcRSAMvalue(measurement_values):
    if len(measurement_values) == 0:
        return 0
    offset = np.mean(measurement_values)
    foo = np.subtract(offset, measurement_values)
    foo = np.abs(foo)
    rasam = np.mean(foo)
    return rasam


class TestRSAMFunction(unittest.TestCase):
    def test_with_example_data(self):
        """inputs fixed array with measurement data; checks if input has been modified"""
        # define input and output arrays bevore each function call
        # to make sure it is not modified by the function itself
        input_a = 7425, 7687, 7687, 7637, 7951, 7813, 7732, 7894, 8573, 8660, 8224, 8780, 8918, 8863, 8837, 8451, 8526, 8931, 9029, 9101, 9322, 9314, 8993, 8681, 8363
        self.assertEqual(calcRSAMvalue(input_a),491.87839999999994)
        check_a = 7425, 7687, 7687, 7637, 7951, 7813, 7732, 7894, 8573, 8660, 8224, 8780, 8918, 8863, 8837, 8451, 8526, 8931, 9029, 9101, 9322, 9314, 8993, 8681, 8363
        self.assertEqual(input_a,check_a)

        input_b = 7425, 7687, 7687, 7637, 7951, 7813, 7732, 7894, 8573, 8660, 8224, 8780, 8918, 8863, 8837, 8451, 8526, 8931, 9029, 9101, 9322, 9314, 8993, 8681, 8363
        self.assertEqual(calcRSAMvalue_withoutNumpy(input_b),491.87839999999994)
        check_b = 7425, 7687, 7687, 7637, 7951, 7813, 7732, 7894, 8573, 8660, 8224, 8780, 8918, 8863, 8837, 8451, 8526, 8931, 9029, 9101, 9322, 9314, 8993, 8681, 8363
        self.assertEqual(input_b,check_b)

    def test_with_zero_elements(self):
        """inputs array with zero elements"""
        self.assertEqual(calcRSAMvalue([]),0)
        self.assertEqual(calcRSAMvalue_withoutNumpy([]),0)



if __name__ == "__main__":
    unittest.main(verbosity=2)
