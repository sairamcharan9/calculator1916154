"""Integration tests for CLI/REPL logic (basic simulation)."""

import pytest
from app.calculator import Calculator

# Editor: ##@sb2853.njit.edu
import sys
import pytest
from app.calculator import Calculator
from main import cli_mode

@pytest.mark.parametrize("operation,num1,num2,expected", [
    ("addition", 5, 3, 8),
    ("subtract", 10, 2, 8),
    ("multiply", 4, 5, 20),
    ("division", 20, 4, 5),
])
def test_compute_operations(operation, num1, num2, expected):
    result = Calculator.compute(operation, num1, num2)
    assert result == expected

@pytest.mark.parametrize("a_string, b_string, operation_string, expected_output", [
    ("5", "3", 'add', "The result of 5 add 3 is equal to 8"),
    ("10", "2", 'subtract', "The result of 10 subtract 2 is equal to 8"),
    ("4", "5", 'multiply', "The result of 4 multiply 5 is equal to 20"),
    ("20", "4", 'divide', "The result of 20 divide 4 is equal to 5"),
    ("1", "0", 'divide', "Cannot divide by zero."),
    ("9", "3", 'unknown', "Unknown operation: unknown"),
    ("a", "3", 'add', "Invalid numeric input."),
    ("5", "b", 'subtract', "Invalid numeric input.")
])
def test_cli_calculation_cases(a_string, b_string, operation_string, expected_output, capsys, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["main.py", a_string, b_string, operation_string])
    try:
        cli_mode()
    except SystemExit:
        pass
    captured = capsys.readouterr()
    assert expected_output in captured.out

# Division by zero
@pytest.mark.parametrize("operation,num1,num2", [
    ("division", 1, 0),
])
def test_division_by_zero(operation, num1, num2):
    with pytest.raises(ZeroDivisionError):
        Calculator.compute(operation, num1, num2)
