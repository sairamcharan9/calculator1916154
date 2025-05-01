"""
Unit tests for Calculator and Calculation classes (core logic, history, and command pattern).
"""
import os
import sys
import pytest
import tempfile
from io import StringIO
from unittest.mock import patch, MagicMock
from src.calculator import Calculator, Calculation
from src.operations.operations import Operations

# Fixture to clear history before each test
@pytest.fixture(autouse=True)
def clear_calculator_history():
    Calculator.clear_history()
    Calculator.undo_stack = []

# Calculation class tests
def test_calculation_str():
    calc = Calculation("add", 2, 3, 5)
    assert str(calc) == "2 add 3 = 5"

def test_calculation_repr_and_eq():
    calc1 = Calculation("add", 2, 3, 5)
    calc2 = Calculation("add", 2, 3, 5)
    calc3 = Calculation("sub", 2, 3, -1)
    assert repr(calc1) == "Calculation(add, 2, 3, 5)"
    assert calc1 == calc2
    assert calc1 != calc3
    assert calc1 != 5  # Not equal to non-Calculation

# Calculator history tests
def test_add_to_history_and_get_history():
    calc = Calculation("add", 2, 3, 5)
    Calculator.add_to_history(calc)
    history = Calculator.get_history()
    assert calc in history

def test_clear_history():
    calc = Calculation("subtract", 5, 2, 3)
    Calculator.add_to_history(calc)
    Calculator.clear_history()
    assert Calculator.get_history() == []

# Input handling tests
def test_get_inputs_valid(monkeypatch):
    inputs = iter(['3', '4'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    num1, num2 = Calculator.get_inputs()
    assert num1 == 3.0
    assert num2 == 4.0

def test_get_inputs_invalid(monkeypatch):
    inputs = iter(['abc', 'quit'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    num1, num2 = Calculator.get_inputs()
    assert num1 is None
    assert num2 is None

# Operation tests
def test_add():
    assert Operations.add(1, 2) == 3

def test_subtract():
    assert Operations.subtract(5, 3) == 2

def test_multiply():
    assert Operations.multiply(4, 2) == 8

def test_divide():
    assert Operations.divide(10, 2) == 5
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
    assert Operations.negate(-2) == 2

def test_reciprocal():
    assert Operations.reciprocal(2) == 0.5
    with pytest.raises(ZeroDivisionError):
        Operations.reciprocal(0)

# REPL simulation helper
def simulate_calculator(monkeypatch, inputs):
    input_iter = iter(inputs)
    monkeypatch.setattr("builtins.input", lambda _: next(input_iter))
    captured_output = StringIO()
    sys_stdout = sys.stdout
    try:
        sys.stdout = captured_output
        Calculator.run()
    except StopIteration:
        pass
    finally:
        sys.stdout = sys_stdout
    return captured_output.getvalue()

class TestCalculation:
    """Tests for the Calculation class."""
    
    def test_calculation_init(self):
        """Test Calculation initialization."""
        calc = Calculation("add", 5, 3, 8)
        assert calc.operation == "add"
        assert calc.num1 == 5
        assert calc.num2 == 3
        assert calc.result == 8
    
    def test_calculation_repr(self):
        """Test Calculation string representation."""
        calc = Calculation("add", 5, 3, 8)
        assert repr(calc) == "Calculation(add, 5, 3, 8)"
    
    def test_calculation_eq(self):
        """Test Calculation equality comparison."""
        calc1 = Calculation("add", 5, 3, 8)
        calc2 = Calculation("add", 5, 3, 8)
        calc3 = Calculation("subtract", 5, 3, 2)
        
        assert calc1 == calc2
        assert calc1 != calc3
        assert calc1 != "not a calculation"

class TestCalculator:
    """Tests for the Calculator class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        Calculator.clear_history()
        Calculator.undo_stack = []
    
    def test_calculator_init(self):
        """Test Calculator initialization."""
        calculator = Calculator()
        assert calculator.history == []
    
    def test_add_to_history(self):
        """Test adding calculations to history."""
        calc = Calculation("add", 2, 3, 5)
        Calculator.add_to_history(calc)
        assert len(Calculator.history) == 1
        assert Calculator.history[0] == calc
    
    def test_clear_history(self):
        """Test clearing calculation history."""
        calc1 = Calculation("add", 2, 3, 5)
        calc2 = Calculation("subtract", 5, 3, 2)
        
        Calculator.add_to_history(calc1)
        Calculator.add_to_history(calc2)
        
        Calculator.clear_history()
        assert len(Calculator.history) == 0
    
    def test_get_history(self):
        """Test getting calculation history."""
        Calculator.clear_history()
        
        calc1 = Calculation("add", 2, 3, 5)
        calc2 = Calculation("subtract", 5, 3, 2)
        
        Calculator.add_to_history(calc1)
        Calculator.add_to_history(calc2)
        
        history = Calculator.get_history()
        
        assert len(history) == 2
        assert history[0] == calc1
        assert history[1] == calc2
        
        # Check that we get a copy
        history.append("new item")
        assert len(Calculator.history) == 2
    
    def test_undo(self):
        """Test undoing a calculation."""
        Calculator.clear_history()
        Calculator.undo_stack = []
        
        calc1 = Calculation("add", 2, 3, 5)
        calc2 = Calculation("multiply", 4, 5, 20)
        
        Calculator.add_to_history(calc1)
        Calculator.add_to_history(calc2)
        
        result = Calculator.undo()
        
        assert result == calc2
        assert len(Calculator.history) == 1
        assert len(Calculator.undo_stack) == 1
        assert Calculator.undo_stack[0] == calc2

    def test_undo_empty_history(self):
        """Test undoing with empty history."""
        Calculator.clear_history()
        Calculator.undo_stack = []
        
        result = Calculator.undo()
        
        assert result is None
        assert len(Calculator.history) == 0
        assert len(Calculator.undo_stack) == 0

class TestCalculatorWithRandomData:
    """Tests for Calculator using random data."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.calculator = Calculator()
    
    def test_random_calculations(self, faker, num_records):
        """Test calculator with random calculations."""
        operations = ["add", "subtract", "multiply", "divide", "power"]
        for _ in range(num_records):
            num1 = faker.pyfloat(min_value=-100, max_value=100)
            num2 = faker.pyfloat(min_value=-100, max_value=100) if faker.boolean() else None
            if num2 == 0:
                num2 = 1
            operation = faker.random_element(operations)
            if num2 is None and operation in ["add", "subtract", "multiply", "divide"]:
                continue
            if operation == "add":
                result = num1 + num2
            elif operation == "subtract":
                result = num1 - num2
            elif operation == "multiply":
                result = num1 * num2
            elif operation == "divide":
                if num2 == 0:
                    continue
                result = num1 / num2
            elif operation == "power":
                if num2 is not None:
                    num2 = max(min(num2, 5), -5)
                    result = num1 ** num2
                else:
                    continue
            calc = Calculation(operation, num1, num2, result)
            Calculator.add_to_history(calc)
            assert calc in Calculator.history

def test_undo_redo_empty():
    Calculator.clear_history()
    assert Calculator.undo() is None
    assert Calculator.redo() is None

def test_compute_invalid():
    with pytest.raises(Exception):
        Calculator.compute("not_a_real_op", 2, 3)

def test_save_and_load_history(tmp_path):
    Calculator.clear_history()
    calc = Calculation("add", 1, 2, 3)
    Calculator.add_to_history(calc)
    file_path = tmp_path / "history.csv"
    Calculator.save_history(str(file_path))
    Calculator.clear_history()
    assert Calculator.get_history() == []
    Calculator.load_history(str(file_path))
    assert Calculator.get_history()[0] == calc

def test_load_history_missing_file():
    Calculator.clear_history()
    with pytest.raises(FileNotFoundError):
        Calculator.load_history("nonexistent_file.csv")
