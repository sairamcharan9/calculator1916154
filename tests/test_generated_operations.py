
"""Property-based tests for Calculator operations using Faker-generated random data."""
# Editor: ##@sb2853.njit.edu

import pytest
from app.calculator import Calculator
from tests.test_utils import generate_test_data


import pytest
from app.calculator import Calculator

def test_generated_operations_property(num1, num2, operation, expected_result):
    """Property-based test for Calculator operations using generated data."""
    if operation == "division" and float(num2) == 0:
        with pytest.raises(ZeroDivisionError):
            Calculator.compute(operation, float(num1), float(num2))
    else:
        result = Calculator.compute(operation, float(num1), float(num2))
        assert pytest.approx(result, rel=1e-9) == float(expected_result)


