"""
Module: calculator
Implements the Calculator and Calculation classes with REPL and history.
"""

from app.operations import Operations
from typing import List, Optional

class Calculation:
    """
    Stores a single arithmetic calculation (operation, operands, result).
    """
    def __init__(self, operation: str, num1: float, num2: float, result: float):
        """
        Initialize a Calculation instance.

        Args:
            operation (str): The operation name (e.g. 'addition').
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


class Calculator:
    """
    Provides a REPL and CLI interface for arithmetic operations.
    """
    history: List[Calculation] = []

    @classmethod
    def run(cls):
        """
        Start the calculator REPL loop.
        """
        print("=========== Calculator Menu ===========")
        print("1) addition")
        print("2) subtract")
        print("3) multiply")
        print("4) division")
        print("5) history (view past calculations)")
        print("6) clear   (clear calculation history)")
        print("7) quit    (exit the calculator)")

        while True:
            choice = input("Enter your choice (1-7): ").strip()
            if choice == "7" or choice.lower() == "quit":
                print("Exiting calculator. Goodbye!")
                break

            if choice == "5":
                print(cls.get_history())
                continue
            if choice == "6":
                cls.clear_history()
                print("History has been cleared.")
                continue

            operation_map = {
                "1": "addition",
                "2": "subtract",
                "3": "multiply",
                "4": "division"
            }
            operation = operation_map.get(choice)
            if not operation:
                print("Invalid choice. Please enter a number from 1 to 7.")
                continue

            num1, num2 = cls.get_inputs()
            if num1 is None or num2 is None:
                print("Invalid input. Please enter valid numbers.")
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

    @classmethod
    def compute(cls, operation: str, num1: float, num2: float) -> float:
        """
        Perform an arithmetic operation on two floats.
        """
        operation_map = {
            "addition": Operations.add,
            "subtract": Operations.subtract,
            "multiply": Operations.multiply,
            "division": Operations.divide,
        }
        if operation not in operation_map:
            raise ValueError(f"Unsupported operation: {operation}")
        return operation_map[operation](num1, num2)

    @classmethod
    def add_to_history(cls, calculation: Calculation):
        """
        Add a Calculation object to the history list.

        Args:
            calculation (Calculation): The calculation to store.
        """
        cls.history.append(calculation)

    @classmethod
    def clear_history(cls):
        """
        Clear the calculation history.
        """
        cls.history.clear()
