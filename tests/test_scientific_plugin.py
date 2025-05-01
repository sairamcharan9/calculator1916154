import pytest
import math
from src.plugins.scientific import (
    power, factorial, AbsoluteCommand, SquareRootCommand, ExponentialCommand,
    LogCommand, LogBaseCommand, FactorialCommand, register_commands
)

# --- Arithmetic function tests ---
def test_power():
    assert power(2, 3) == 8
    assert power(5, 0) == 1
    assert power(9, 0.5) == 3

def test_factorial_valid():
    assert factorial(0) == 1
    assert factorial(1) == 1
    assert factorial(5) == 120
    assert factorial(3.0) == 6

def test_factorial_negative():
    with pytest.raises(ValueError):
        factorial(-1)

def test_factorial_non_integer():
    with pytest.raises(ValueError):
        factorial(2.5)

# --- Command class tests ---
def test_absolute_command():
    cmd = AbsoluteCommand()
    assert cmd.name == "abs"
    assert cmd.execute(-3) == 3
    assert cmd.execute(5) == 5

def test_square_root_command():
    cmd = SquareRootCommand()
    assert cmd.name == "sqrt"
    assert cmd.execute(4) == 2
    assert cmd.execute(0) == 0
    with pytest.raises(ValueError):
        cmd.execute(-9)

def test_exponential_command():
    cmd = ExponentialCommand()
    assert cmd.name == "exp"
    assert math.isclose(cmd.execute(1), math.exp(1))

# LogCommand

def test_log_command():
    cmd = LogCommand()
    assert cmd.name == "log"
    assert math.isclose(cmd.execute(math.e), 1)
    with pytest.raises(ValueError):
        cmd.execute(0)
    with pytest.raises(ValueError):
        cmd.execute(-5)

# LogBaseCommand

def test_logbase_command():
    cmd = LogBaseCommand()
    assert cmd.name == "logbase"
    assert math.isclose(cmd.execute(100, 10), 2)
    with pytest.raises(ValueError):
        cmd.execute(0, 10)
    with pytest.raises(ValueError):
        cmd.execute(10, 1)
    with pytest.raises(ValueError):
        cmd.execute(10, -2)

# FactorialCommand

def test_factorial_command():
    cmd = FactorialCommand()
    assert cmd.name == "factorial"
    assert cmd.execute(4) == 24
    with pytest.raises(ValueError):
        cmd.execute(-3)
    with pytest.raises(ValueError):
        cmd.execute(2.2)

# Plugin registry/registration

def test_register_commands():
    registry = {}
    register_commands(registry)
    assert "abs" in registry
    assert "sqrt" in registry
    assert "exp" in registry
    assert "log" in registry
    assert "logbase" in registry
    assert "factorial" in registry
