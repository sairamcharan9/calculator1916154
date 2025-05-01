"""
Power command implementation for the calculator.
"""

from src.commands.command_base import Command
from src.calculator import Calculator, Calculation
import logging

class PowerCommand(Command):
    """Command to calculate x raised to the power of y."""
    
    @property
    def name(self) -> str:
        return "power"
    
    def execute(self, num1: float, num2: float) -> float:
        """
        Execute power operation (x^y) and add to history.
        
        Args:
            num1 (float): Base number
            num2 (float): Exponent
            
        Returns:
            float: Result of the power operation
        """
        try:
            # Calculate power operation using ** operator
            result = num1 ** num2
            # Add calculation to history
            Calculator.add_to_history(Calculation("power", num1, num2, result))
            logging.info(f"Power operation executed: {num1}^{num2} = {result}")
            return result
        except Exception as e:
            logging.error(f"Error in power operation: {e}")
            raise
