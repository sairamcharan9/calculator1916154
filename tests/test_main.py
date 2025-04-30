# test_main.py for testing main.py
# Copying from calc_app for full test coverage
import sys
import pytest
from calculator import Calculator
from decimal import Decimal

# Example test for main.py functionality
# Add more tests as in calc_app/test_main.py if needed

import sys
import pytest
from calculator import Calculator
from decimal import Decimal

def run_main_with_args(args):
    sys.argv = ["main.py"] + args
    from main import main
    main()

def test_add(capsys):
    run_main_with_args(["5", "3", "add"])
    captured = capsys.readouterr()
    assert "The result of 5 add 3 is equal to 8" in captured.out

def test_subtract(capsys):
    run_main_with_args(["10", "2", "subtract"])
    captured = capsys.readouterr()
    assert "The result of 10 subtract 2 is equal to 8" in captured.out

def test_multiply(capsys):
    run_main_with_args(["4", "5", "multiply"])
    captured = capsys.readouterr()
    assert "The result of 4 multiply 5 is equal to 20" in captured.out

def test_divide(capsys):
    run_main_with_args(["20", "4", "divide"])
    captured = capsys.readouterr()
    assert "The result of 20 divide 4 is equal to 5" in captured.out

def test_divide_by_zero(capsys):
    run_main_with_args(["1", "0", "divide"])
    captured = capsys.readouterr()
    assert "An error occurred: Cannot divide by zero" in captured.out

def test_unknown_operation(capsys):
    run_main_with_args(["9", "3", "unknown"])
    captured = capsys.readouterr()
    assert "Unknown operation: unknown" in captured.out

def test_invalid_input_a(capsys):
    run_main_with_args(["a", "3", "add"])
    captured = capsys.readouterr()
    assert "Invalid number input: a or 3 is not a valid number." in captured.out

def test_invalid_input_b(capsys):
    run_main_with_args(["5", "b", "subtract"])
    captured = capsys.readouterr()
    assert "Invalid number input: 5 or b is not a valid number." in captured.out
