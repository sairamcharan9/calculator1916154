"""Unit tests for the Operations class."""

# Editor: ##@sb2853.njit.edu
import pytest
from app.operations import Operations

@pytest.mark.parametrize(
    "a, b, expected",
    [(3, 2, 5), (-1, -1, -2), (0, 0, 0), (2, 3, 5), (-1, 1, 0), (0, 0, 0)]
)
def test_add(a, b, expected):
    assert Operations.add(a, b) == expected

@pytest.mark.parametrize(
    "a, b, expected",
    [(5, 2, 3), (0, -1, 1), (-3, -3, 0), (5, 3, 2), (0, 1, -1), (-3, -3, 0)]
)
def test_subtract(a, b, expected):
    assert Operations.subtract(a, b) == expected

@pytest.mark.parametrize(
    "a, b, expected",
    [(3, 3, 9), (-1, 4, -4), (0, 100, 0), (4, 5, 20), (-1, 4, -4), (0, 100, 0)]
)
def test_multiply(a, b, expected):
    assert Operations.multiply(a, b) == expected

@pytest.mark.parametrize(
    "a, b, expected",
    [(6, 2, 3), (-10, 5, -2), (8, 4, 2), (10, 2, 5), (-10, 5, -2), (8, 4, 2)]
)
def test_divide(a, b, expected):
    assert Operations.divide(a, b) == expected

def test_divide_by_zero():
    with pytest.raises(ZeroDivisionError):
        Operations.divide(5, 0)
