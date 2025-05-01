"""
Implementation of arithmetic command classes using the command pattern.
"""

from src.commands.command_base import Command
from src.calculator import Calculator, Calculation
import logging

class AddCommand(Command):
    """Command to execute addition operation."""
    
    @property
    def name(self) -> str:
        return "add"
    
    def execute(self, num1: float, num2: float) -> float:
        """
        Execute addition operation and add to history.
        
        Args:
            num1 (float): First number
            num2 (float): Second number
            
        Returns:
            float: Result of addition
        """
        result = Calculator.compute("add", num1, num2)
        Calculator.add_to_history(Calculation("add", num1, num2, result))
        logging.info(f"Addition executed: {num1} + {num2} = {result}")
        return result


class SubtractCommand(Command):
    """Command to execute subtraction operation."""
    
    @property
    def name(self) -> str:
        return "subtract"
    
    def execute(self, num1: float, num2: float) -> float:
        """
        Execute subtraction operation and add to history.
        
        Args:
            num1 (float): First number
            num2 (float): Second number
            
        Returns:
            float: Result of subtraction
        """
        result = Calculator.compute("subtract", num1, num2)
        Calculator.add_to_history(Calculation("subtract", num1, num2, result))
        logging.info(f"Subtraction executed: {num1} - {num2} = {result}")
        return result


class MultiplyCommand(Command):
    """Command to execute multiplication operation."""
    
    @property
    def name(self) -> str:
        return "multiply"
    
    def execute(self, num1: float, num2: float) -> float:
        """
        Execute multiplication operation and add to history.
        
        Args:
            num1 (float): First number
            num2 (float): Second number
            
        Returns:
            float: Result of multiplication
        """
        result = Calculator.compute("multiply", num1, num2)
        Calculator.add_to_history(Calculation("multiply", num1, num2, result))
        logging.info(f"Multiplication executed: {num1} * {num2} = {result}")
        return result


class DivideCommand(Command):
    """Command to execute division operation."""
    
    @property
    def name(self) -> str:
        return "divide"
    
    def execute(self, num1: float, num2: float) -> float:
        """
        Execute division operation and add to history.
        
        Args:
            num1 (float): First number
            num2 (float): Second number
            
        Returns:
            float: Result of division
            
        Raises:
            ZeroDivisionError: If attempting to divide by zero
        """
        if num2 == 0:
            logging.error("Division by zero attempted")
            raise ZeroDivisionError("Cannot divide by zero.")
            
        result = Calculator.compute("divide", num1, num2)
        Calculator.add_to_history(Calculation("divide", num1, num2, result))
        logging.info(f"Division executed: {num1} / {num2} = {result}")
        return result


class HistoryCommand(Command):
    """Command to display calculation history."""
    
    @property
    def name(self) -> str:
        return "history"
    
    def execute(self) -> str:
        """
        Execute history display command.

        Returns:
            str: String representation of calculation history
        """
        history = Calculator.get_history()
        logging.info("History command executed")
        if not history:
            return "Calculation History:\n(empty)"
        return "Calculation History:\n" + "\n".join(str(calc) for calc in history)


class ClearHistoryCommand(Command):
    """Command to clear calculation history."""
    
    @property
    def name(self) -> str:
        return "clear_history"
    
    def execute(self) -> str:
        """
        Execute clear history command.
        """
        Calculator.clear_history()
        logging.info("History cleared")
        return "History has been cleared."


class UndoCommand(Command):
    """Command to undo last calculation."""
    
    @property
    def name(self) -> str:
        return "undo"
    
    def execute(self) -> str:
        """
        Execute undo command.
        
        Returns:
            str: Message about the undo operation
        """
        calc = Calculator.undo()
        if calc:
            logging.info(f"Undid calculation: {calc}")
            return f"Undone: {calc}"
        logging.info("Nothing to undo")
        return "Nothing to undo."


class RedoCommand(Command):
    """Command to redo last undone calculation."""
    
    @property
    def name(self) -> str:
        return "redo"
    
    def execute(self) -> str:
        """
        Execute redo command.
        
        Returns:
            str: Message about the redo operation
        """
        calc = Calculator.redo()
        if calc:
            logging.info(f"Redid calculation: {calc}")
            return f"Redone: {calc}"
        logging.info("Nothing to redo")
        return "Nothing to redo."
