import pytest
from calculator import Calculator

# This test uses the random_calculations fixture from conftest.py, which generates N random records

def test_calculator_with_faker(random_calculations):
    for a, b, op, expected in random_calculations:
        if op == 'add':
            result = Calculator.add(a, b)
        elif op == 'subtract':
            result = Calculator.subtract(a, b)
        elif op == 'multiply':
            result = Calculator.multiply(a, b)
        elif op == 'divide':
            result = Calculator.divide(a, b)
        else:
            pytest.fail(f"Unknown operation: {op}")
        assert result == expected, f"Failed on {a} {op} {b}: expected {expected}, got {result}"
