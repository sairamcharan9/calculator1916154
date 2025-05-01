"""
Unit tests for operations module.
"""
import pytest
from src.operations.operations import Operations

def test_add():
    assert Operations.add(2, 3) == 5
    assert Operations.add(-1, 1) == 0

def test_subtract():
    assert Operations.subtract(5, 3) == 2
    assert Operations.subtract(0, 1) == -1

def test_multiply():
    assert Operations.multiply(4, 2) == 8
    assert Operations.multiply(-2, -2) == 4

def test_divide():
    assert Operations.divide(6, 2) == 3
    with pytest.raises(ZeroDivisionError):
        Operations.divide(1, 0)

def test_modulus():
    assert Operations.modulus(10, 3) == 1
    with pytest.raises(ZeroDivisionError):
        Operations.modulus(1, 0)

def test_exponentiate():
    assert Operations.exponentiate(2, 3) == 8
    assert Operations.exponentiate(9, 0.5) == 3

def test_sqrt():
    assert Operations.sqrt(16) == 4
    with pytest.raises(ValueError):
        Operations.sqrt(-1)

def test_absolute():
    assert Operations.absolute(-5) == 5
    assert Operations.absolute(5) == 5

def test_negate():
    assert Operations.negate(5) == -5
    assert Operations.negate(-5) == 5

def test_reciprocal():
    assert Operations.reciprocal(2) == 0.5
    with pytest.raises(ZeroDivisionError):
        Operations.reciprocal(0)

def test_sin():
    import math
    assert math.isclose(Operations.sin(math.pi/2), 1, rel_tol=1e-9)

def test_cos():
    import math
    assert math.isclose(Operations.cos(0), 1, rel_tol=1e-9)

def test_tan():
    import math
    assert math.isclose(Operations.tan(0), 0, rel_tol=1e-9)

def test_log10():
    import math
    assert math.isclose(Operations.log10(100), 2, rel_tol=1e-9)
    with pytest.raises(ValueError):
        Operations.log10(0)

def test_ln():
    import math
    assert math.isclose(Operations.ln(math.e), 1, rel_tol=1e-9)
    with pytest.raises(ValueError):
        Operations.ln(0)

def test_exp():
    import math
    assert math.isclose(Operations.exp(1), math.e, rel_tol=1e-9)

def test_factorial():
    assert Operations.factorial(5) == 120
    with pytest.raises(ValueError):
        Operations.factorial(-1)
    with pytest.raises(ValueError):
        Operations.factorial(2.5)

def test_floor():
    assert Operations.floor(2.7) == 2

def test_ceil():
    assert Operations.ceil(2.1) == 3

def test_round():
    assert Operations.round(2.567, 2) == 2.57

def test_percent():
    assert Operations.percent(25, 100) == 25
    with pytest.raises(ZeroDivisionError):
        Operations.percent(1, 0)

def test_mean():
    assert Operations.mean([1,2,3,4,5]) == 3

def test_median():
    assert Operations.median([1,2,3,4,5]) == 3

def test_mode():
    assert Operations.mode([1,1,2,3]) == 1

def test_variance():
    assert Operations.variance([1,2,3,4,5]) == 2.5

def test_stdev():
    import math
    assert math.isclose(Operations.stdev([1,2,3,4,5]), 1.58113883008, rel_tol=1e-9)

def test_minimum():
    assert Operations.minimum([1,2,3]) == 1

def test_maximum():
    assert Operations.maximum([1,2,3]) == 3

def test_total():
    assert Operations.total([1,2,3]) == 6

def test_count():
    assert Operations.count([1,2,3]) == 3
