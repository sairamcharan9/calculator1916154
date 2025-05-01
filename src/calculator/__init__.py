"""
Module: calculator
Implements the Calculator and Calculation classes with REPL and history.
"""

from src.operations.operations import Operations
from typing import List, Dict, Any
import math
import logging

class Calculation:
    """
    Stores a single arithmetic calculation (operation, operands, result).
    """
    def __init__(self, operation: str, num1: float, num2: float, result: float):
        """
        Initialize a Calculation instance.

        Args:
            operation (str): The operation name (e.g. 'add').
            num1 (float): First operand.
            num2 (float): Second operand.
            result (float): Computed result of the operation.
        """
        self.operation = operation
        self.num1 = num1
        self.num2 = num2
        self.result = result

    def __str__(self) -> str:
        return f"{self.num1} {self.operation} {self.num2} = {self.result}"

    def __repr__(self) -> str:
        return f"Calculation({self.operation}, {self.num1}, {self.num2}, {self.result})"

    def __eq__(self, other):
        if not isinstance(other, Calculation):
            return False
        return (
            self.operation == other.operation and
            self.num1 == other.num1 and
            self.num2 == other.num2 and
            self.result == other.result
        )


class Calculator:
    """
    Advanced calculator supporting arithmetic operations and undo/redo functionality.
    """
    history: List[Calculation] = []
    undo_stack: List[Calculation] = []

    @classmethod
    def get_history(cls) -> list:
        """
        Return the calculation history as a list of Calculation objects.
        Returns:
            list: All Calculation objects in history.
        """
        return cls.history

    @classmethod
    def format_history(cls) -> str:
        """
        Return a string representation of the calculation history for display.
        Returns:
            str: All calculations in history, or 'No calculations recorded.' if empty.
        """
        if not cls.history:
            return "No calculations recorded."
        return "\n".join(str(calc) for calc in cls.history)

    @classmethod
    def add_to_history(cls, calculation: 'Calculation') -> None:
        """
        Add a Calculation object to the calculation history.

        Args:
            calculation (Calculation): The Calculation object to add.
        """
        cls.history.append(calculation)

    @classmethod
    def clear_history(cls):
        """
        Clear the calculation history and undo stack.
        """
        cls.history.clear()
        cls.undo_stack.clear()
        logging.info("Cleared calculation history and undo stack")

    @classmethod
    def undo(cls):
        """
        Undo the last calculation if available.
        
        Returns:
            Calculation or None: The undone calculation, or None if none available
        """
        if cls.history:
            calc = cls.history.pop()
            cls.undo_stack.append(calc)
            logging.info(f"Undid calculation: {calc}")
            return calc
        logging.info("Nothing to undo")
        return None

    @classmethod
    def redo(cls):
        """
        Redo the last undone calculation if available.
        
        Returns:
            Calculation or None: The redone calculation, or None if none available
        """
        if cls.undo_stack:
            calc = cls.undo_stack.pop()
            cls.history.append(calc)
            logging.info(f"Redid calculation: {calc}")
            return calc
        logging.info("Nothing to redo")
        return None

    @classmethod
    def save_history(cls, filename: str) -> None:
        """
        Save calculation history to a CSV file.

        Args:
            filename (str): The file path to save the history.
        """
        import pandas as pd
        data = [
            {
                'operation': calc.operation,
                'num1': calc.num1,
                'num2': calc.num2,
                'result': calc.result
            }
            for calc in cls.history
        ]
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)

    @classmethod
    def load_history(cls, filename: str) -> None:
        """
        Load calculation history from a CSV file.

        Args:
            filename (str): The file path to load the history from.
        """
        import pandas as pd
        df = pd.read_csv(filename)
        cls.history = [
            Calculation(
                row['operation'],
                row['num1'],
                row['num2'],
                row['result']
            )
            for _, row in df.iterrows()
        ]

    @classmethod
    def compute(cls, operation: str, num1: float, num2: float = None) -> float:
        """
        Compute the result of an operation. Supports arithmetic operations.
        
        Args:
            operation (str): Operation name
            num1 (float): First operand
            num2 (float, optional): Second operand, not needed for unary operations
            
        Returns:
            float: Computation result
            
        Raises:
            ValueError: If operation is not supported
            ZeroDivisionError: If trying to divide by zero
        """
        try:
            if operation == 'add':
                return Operations.add(num1, num2)
            elif operation == 'subtract':
                return Operations.subtract(num1, num2)
            elif operation == 'multiply':
                return Operations.multiply(num1, num2)
            elif operation == 'divide':
                return Operations.divide(num1, num2)
            elif operation == 'sqrt':
                return math.sqrt(num1)
            elif operation == 'log':
                return math.log(num1)
            elif operation == 'sin':
                return math.sin(num1)
            elif operation == 'cos':
                return math.cos(num1)
            elif operation == 'tan':
                return math.tan(num1)
            else:
                raise ValueError(f"Unsupported operation: {operation}")
        except Exception as e:
            logging.error(f"Error computing {operation}: {e}")
            raise

    @classmethod
    def run(cls):
        """
        Start the calculator REPL loop.
        """
        print("=========== Calculator Menu ===========")
        print("1) add")
        print("2) subtract")
        print("3) multiply")
        print("4) divide")
        print("5) history (view past calculations)")
        print("6) clear   (clear calculation history)")
        print("7) undo    (undo last calculation)")
        print("8) redo    (redo last undone calculation)")
        print("9) sqrt    (square root)")
        print("10) log    (natural logarithm)")
        print("11) sin    (sine)")
        print("12) cos    (cosine)")
        print("13) tan    (tangent)")
        print("14) quit    (exit the calculator)")

        while True:
            choice = input("Enter your choice (1-14): ").strip()
            if choice == "14" or choice.lower() == "quit":
                print("Exiting calculator. Goodbye!")
                break

            if choice == "5":
                print(cls.format_history())
                continue
            if choice == "6":
                cls.clear_history()
                print("History has been cleared.")
                continue
            if choice == "7":
                cls.undo()
                continue
            if choice == "8":
                cls.redo()
                continue

            operation_map = {
                "1": "add",
                "2": "subtract",
                "3": "multiply",
                "4": "divide",
                "9": "sqrt",
                "10": "log",
                "11": "sin",
                "12": "cos",
                "13": "tan"
            }
            operation = operation_map.get(choice)
            if not operation:
                print("Invalid choice. Please enter a number from 1 to 14.")
                continue

            if operation in ["sqrt", "log", "sin", "cos", "tan"]:
                num1 = float(input("Enter the first number: ").strip())
                try:
                    result = cls.compute(operation, num1)
                    print(f"The result is: {result}")
                    cls.add_to_history(Calculation(operation, num1, 0, result))
                except ZeroDivisionError:
                    print("Cannot divide by zero.")
                except ValueError as e:
                    print(e)
            else:
                num1, num2 = cls.get_inputs()
                if num1 is None or num2 is None:
                    print("Invalid number. Please enter numeric values.")
                    continue

                try:
                    result = cls.compute(operation, num1, num2)
                    print(f"The result is: {result}")
                    cls.add_to_history(Calculation(operation, num1, num2, result))
                except ZeroDivisionError:
                    print("Cannot divide by zero.")
                except ValueError as e:
                    print(e)

    @staticmethod
    def get_inputs() -> (float, float):
        """
        Prompt for two numeric inputs.
        Returns:
            (float | None, float | None): The two numbers, or (None, None) if quitting/invalid.
        """
        first = input("Enter the first number: ").strip()
        if first.lower() == "quit":
            print("Exiting calculator. Goodbye!")
            return None, None
        second = input("Enter the second number: ").strip()
        if second.lower() == "quit":
            print("Exiting calculator. Goodbye!")
            return None, None
        try:
            return float(first), float(second)
        except ValueError:
            return None, None
