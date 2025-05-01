<<<<<<< HEAD
"""Unit tests for the Calculator and Calculation classes, including REPL simulation and edge cases."""
# Editor: ##@sb2853.njit.edu

import pytest
import sys
from io import StringIO
from app.calculator import Calculator, Calculation

@pytest.fixture(autouse=True)
def clear_calculator_history():
    Calculator.clear_history()

def simulate_calculator(monkeypatch, inputs):
    input_iter = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_iter))
    captured_output = StringIO()
    sys.stdout = captured_output
    try:
        Calculator.run()
    except StopIteration:
        pass  # Allow test to finish if input runs out
    finally:
        sys.stdout = sys.__stdout__
    return captured_output.getvalue()

def test_calculation_str():
    calc = Calculation("addition", 2, 3, 5)
    assert str(calc) == "2 addition 3 = 5"

def test_add_to_history_and_get_history():
    Calculator.history.clear()
    calc = Calculation("addition", 2, 3, 5)
    Calculator.add_to_history(calc)
    history = Calculator.get_history()
    assert "2 addition 3 = 5" in history

def test_clear_history():
    Calculator.history.clear()
    calc = Calculation("subtract", 5, 2, 3)
    Calculator.add_to_history(calc)
    Calculator.clear_history()
    assert Calculator.get_history() == "No calculations recorded."

def test_start_and_quit(monkeypatch):
=======
import pytest
import sys
from io import StringIO
from app.calculator import Calculator


@pytest.fixture(autouse=True)
def clear_calculator_history():
    """Ensure calculator history is cleared before each test."""
    Calculator.clear_history()


def simulate_calculator(monkeypatch, inputs):
    """
    Helper function to simulate user input for the calculator REPL.

    Args:
        monkeypatch: Pytest fixture to override input().
        inputs (list[str]): A list of strings to feed as user input.

    Returns:
        str: Captured output from the REPL session.
    """
    input_iter = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_iter))

    captured_output = StringIO()
    sys.stdout = captured_output
    Calculator.run()
    sys.stdout = sys.__stdout__
    return captured_output.getvalue()


def test_start_and_quit(monkeypatch):
    """Test that '7' quits the calculator."""
>>>>>>> origin/version5
    output = simulate_calculator(monkeypatch, ["7"])
    assert "Calculator Menu" in output
    assert "Exiting calculator. Goodbye!" in output

<<<<<<< HEAD
def test_addition(monkeypatch):
    output = simulate_calculator(monkeypatch, ["1", "3", "2", "7"])
    assert "The result is: 5.0" in output

def test_subtraction(monkeypatch):
    output = simulate_calculator(monkeypatch, ["2", "10", "4", "7"])
    assert "The result is: 6.0" in output

def test_multiplication(monkeypatch):
    output = simulate_calculator(monkeypatch, ["3", "2", "3", "7"])
    assert "The result is: 6.0" in output

def test_division(monkeypatch):
    output = simulate_calculator(monkeypatch, ["4", "8", "2", "7"])
    assert "The result is: 4.0" in output

def test_division_by_zero(monkeypatch):
    output = simulate_calculator(monkeypatch, ["4", "8", "0", "7"])
    assert "Cannot divide by zero." in output

def test_invalid_number_input(monkeypatch):
    output = simulate_calculator(monkeypatch, ["1", "abc", "3", "7"])
    assert "Invalid input. Please enter valid numbers." in output

def test_quit_during_number_input(monkeypatch):
    output = simulate_calculator(monkeypatch, ["1", "quit"])
    assert "Exiting calculator. Goodbye!" in output

def test_invalid_choice(monkeypatch):
    output = simulate_calculator(monkeypatch, ["99", "7"])
    assert "Invalid choice. Please enter a number from 1 to 7." in output

def test_history(monkeypatch):
    output = simulate_calculator(monkeypatch, ["5", "7"])
    assert "No calculations recorded." in output

def test_clear_history_via_repl(monkeypatch):
    output = simulate_calculator(monkeypatch, ["6", "7"])
    assert "History has been cleared." in output

def test_history_after_addition(monkeypatch):
    output = simulate_calculator(monkeypatch, ["1", "3", "2", "5", "7"])
    assert "3.0 addition 2.0 = 5.0" in output

def test_clear_history_then_check(monkeypatch):
=======

def test_addition(monkeypatch):
    """Test that '1' performs addition."""
    output = simulate_calculator(monkeypatch, ["1", "3", "2", "7"])
    assert "The result is: 5.0" in output


def test_subtraction(monkeypatch):
    """Test that '2' performs subtraction."""
    output = simulate_calculator(monkeypatch, ["2", "10", "4", "7"])
    assert "The result is: 6.0" in output


def test_multiplication(monkeypatch):
    """Test that '3' performs multiplication."""
    output = simulate_calculator(monkeypatch, ["3", "2", "3", "7"])
    assert "The result is: 6.0" in output


def test_division(monkeypatch):
    """Test that '4' performs division."""
    output = simulate_calculator(monkeypatch, ["4", "8", "2", "7"])
    assert "The result is: 4.0" in output


def test_division_by_zero(monkeypatch):
    """Test division by zero handling."""
    output = simulate_calculator(monkeypatch, ["4", "8", "0", "7"])
    assert "Cannot divide by zero." in output


def test_invalid_number_input(monkeypatch):
    """Test entering a non-numeric value triggers invalid number message."""
    output = simulate_calculator(monkeypatch, ["1", "abc", "3", "7"])
    assert "Invalid number. Please enter numeric values." in output


def test_quit_during_number_input(monkeypatch):
    """Test typing 'quit' during number input."""
    output = simulate_calculator(monkeypatch, ["1", "quit"])
    assert "Exiting calculator. Goodbye!" in output


def test_invalid_choice(monkeypatch):
    """Test an unrecognized menu choice prints an error."""
    output = simulate_calculator(monkeypatch, ["99", "7"])
    assert "Invalid choice. Please enter a number from 1 to 7." in output


def test_history(monkeypatch):
    """Test viewing history when empty."""
    output = simulate_calculator(monkeypatch, ["5", "7"])
    assert "No calculations recorded." in output


def test_clear_history_via_repl(monkeypatch):
    """Test clearing history via the REPL."""
    output = simulate_calculator(monkeypatch, ["6", "7"])
    assert "History has been cleared." in output


def test_stoptest_command(monkeypatch):
    """Test the hidden '8' command for coverage."""
    output = simulate_calculator(monkeypatch, ["8"])
    assert "Testing coverage for final line." in output


def test_history_after_addition(monkeypatch):
    """Test that history is updated after an addition operation."""
    output = simulate_calculator(monkeypatch, ["1", "3", "2", "5", "7"])
    assert "3.0 addition 2.0 = 5.0" in output


def test_clear_history_direct(capsys):
    """Test clearing history directly."""
    Calculator.clear_history()
    captured = capsys.readouterr()
    assert "History has been cleared." in captured.out


def test_quit_as_first_number(monkeypatch):
    """Test typing 'quit' as the first number input."""
    output = simulate_calculator(monkeypatch, ["1", "quit"])
    assert "Exiting calculator. Goodbye!" in output


def test_clear_history_then_check(monkeypatch):
    """Test clearing history and checking it's empty."""
>>>>>>> origin/version5
    output = simulate_calculator(monkeypatch, ["6", "5", "7"])
    assert "History has been cleared." in output
    assert "No calculations recorded." in output

<<<<<<< HEAD
def test_get_inputs_invalid(monkeypatch):
=======

# ===================== TESTS TO COVER LINE 119, 177, 199 ======================

def test_get_inputs_first_number_quit(monkeypatch):
    """Covers the case when the user types 'quit' as the first number input."""
    inputs = iter(["quit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    num1, num2 = Calculator.get_inputs()
    assert num1 is None
    assert num2 is None


def test_get_inputs_second_number_quit(monkeypatch):
    """Covers line 119: Returning None, None when 'quit' is entered as the second number."""
    inputs = iter(["5", "quit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    num1, num2 = Calculator.get_inputs()
    assert num1 is None
    assert num2 is None


def test_get_inputs_invalid(monkeypatch):
    """Covers the case when invalid input is provided for number entry."""
>>>>>>> origin/version5
    inputs = iter(["abc", "quit"])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    num1, num2 = Calculator.get_inputs()
    assert num1 is None
    assert num2 is None

<<<<<<< HEAD
def test_compute_invalid_operation():
=======

def test_compute_invalid_operation():
    """Covers line 177: Raises ValueError for unsupported operations."""
>>>>>>> origin/version5
    with pytest.raises(ValueError, match="Unsupported operation: unknown"):
        Calculator.compute("unknown", 5, 3)
