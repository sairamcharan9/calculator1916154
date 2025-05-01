"""
Scientific operations plugin module.
Provides advanced mathematical operations for the calculator.
"""

import logging
import math
from src.commands.command_base import Command
from src.calculator import Calculator, Calculation

# Get logger
logger = logging.getLogger('calculator.plugins.scientific')

def power(x, y):
    """
    Return x raised to the power y.
    
    Args:
        x (float): Base
        y (float): Exponent
        
    Returns:
        float: Result of x^y
    """
    return x ** y

def factorial(x):
    """
    Return the factorial of x.
    
    Args:
        x (int): Number to calculate factorial of
        
    Returns:
        int: Factorial result
        
    Raises:
        ValueError: If x is negative or not an integer
    """
    if not isinstance(x, int) and not x.is_integer():
        raise ValueError("Factorial requires an integer")
    
    if x < 0:
        raise ValueError("Factorial not defined for negative numbers")
    
    if x == 0 or x == 1:
        return 1
    else:
        return x * factorial(x - 1)

# Plugin registry for dynamic discovery
PLUGIN_REGISTRY = {
    'power': power,
    'factorial': factorial
}

class AbsoluteCommand(Command):
    """Command to calculate the absolute value of a number."""
    
    @property
    def name(self) -> str:
        return "abs"
    
    def execute(self, num: float) -> float:
        """
        Execute absolute value operation.
        
        Args:
            num (float): Number to find absolute value of
            
        Returns:
            float: Absolute value result
        """
        result = abs(num)
        Calculator.add_to_history(Calculation("abs", num, None, result))
        logger.info(f"Absolute value operation executed: |{num}| = {result}")
        return result

class SquareRootCommand(Command):
    """Command to calculate the square root of a number."""
    
    @property
    def name(self) -> str:
        return "sqrt"
    
    def execute(self, num: float) -> float:
        """
        Execute square root operation.
        
        Args:
            num (float): Number to find square root of
            
        Returns:
            float: Square root result
            
        Raises:
            ValueError: If attempting to find square root of negative number
        """
        if num < 0:
            raise ValueError("Cannot calculate square root of negative number")
        result = math.sqrt(num)
        Calculator.add_to_history(Calculation("sqrt", num, None, result))
        logger.info(f"Square root operation executed: √{num} = {result}")
        return result

class ExponentialCommand(Command):
    """Command to calculate e raised to the power of x."""
    
    @property
    def name(self) -> str:
        return "exp"
    
    def execute(self, num: float) -> float:
        """
        Execute exponential operation.
        
        Args:
            num (float): Exponent
            
        Returns:
            float: Result of e^x
        """
        result = math.exp(num)
        Calculator.add_to_history(Calculation("exp", num, None, result))
        logger.info(f"Exponential operation executed: e^{num} = {result}")
        return result

class LogCommand(Command):
    """Command to calculate the natural logarithm of a number."""
    
    @property
    def name(self) -> str:
        return "log"
    
    def execute(self, num: float) -> float:
        """
        Execute natural logarithm operation.
        
        Args:
            num (float): Number to find logarithm of
            
        Returns:
            float: Natural logarithm result
            
        Raises:
            ValueError: If num is less than or equal to zero
        """
        if num <= 0:
            raise ValueError("Cannot calculate logarithm of non-positive number")
        result = math.log(num)
        Calculator.add_to_history(Calculation("log", num, None, result))
        logger.info(f"Natural logarithm operation executed: ln({num}) = {result}")
        return result

class LogBaseCommand(Command):
    """Command to calculate the logarithm of a number with a specified base."""
    
    @property
    def name(self) -> str:
        return "logbase"
    
    def execute(self, num: float, base: float) -> float:
        """
        Execute logarithm with base operation.
        
        Args:
            num (float): Number to find logarithm of
            base (float): Logarithm base
            
        Returns:
            float: Logarithm result
            
        Raises:
            ValueError: If num is less than or equal to zero or base is invalid
        """
        if num <= 0:
            raise ValueError("Cannot calculate logarithm of non-positive number")
        if base <= 0 or base == 1:
            raise ValueError("Logarithm base must be positive and not equal to 1")
        result = math.log(num, base)
        Calculator.add_to_history(Calculation("logbase", num, base, result))
        logger.info(f"Logarithm operation executed: log_{base}({num}) = {result}")
        return result

class FactorialCommand(Command):
    """Command to calculate factorial of a number."""
    
    @property
    def name(self) -> str:
        return "factorial"
    
    def execute(self, num: float) -> float:
        """
        Execute factorial operation.
        
        Args:
            num (float): Number to find factorial of
            
        Returns:
            float: Factorial result
            
        Raises:
            ValueError: If num is negative or not an integer
        """
        if not isinstance(num, int) and not num.is_integer():
            raise ValueError("Factorial requires an integer")
        if num < 0:
            raise ValueError("Factorial not defined for negative numbers")
        
        result = factorial(int(num))
        Calculator.add_to_history(Calculation("factorial", num, None, result))
        logger.info(f"Factorial operation executed: {num}! = {result}")
        return result

def register_commands(command_registry):
    """
    Register scientific commands to the global command registry.
    
    Args:
        command_registry (dict): The global command registry
    """
    # Import PowerCommand here to avoid circular imports at module level
    from src.commands.power_command import PowerCommand
    
    scientific_commands = [
        PowerCommand(),  # Include PowerCommand in the list
        AbsoluteCommand(),
        SquareRootCommand(),
        ExponentialCommand(),
        LogCommand(),
        LogBaseCommand(),
        FactorialCommand(),
    ]
    
    for cmd in scientific_commands:
        command_registry[cmd.name] = cmd
        logger.info(f"Registered scientific command: {cmd.name}")
    
    return [cmd.name for cmd in scientific_commands]

# Import for type checking only, not for instantiation
from src.commands.power_command import PowerCommand as PowerCommandType
