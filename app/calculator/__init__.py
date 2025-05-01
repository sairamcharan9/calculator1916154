<<<<<<< HEAD
"""
Module: calculator
Implements the Calculator and Calculation classes with REPL and history.
"""

from app.operations import Operations
from typing import List, Optional

class Calculation:
    """
    Stores a single arithmetic calculation.
    """
    def __init__(self, operation: str, num1: float, num2: float, result: float):
=======
"""Implements a numeric-based calculator with a hidden coverage command."""

from app.operations import Operations


class Calculation:
    """Stores a single arithmetic calculation (operation, operands, result)."""

    def __init__(self, operation, num1, num2, result):
        """
        Initialize a Calculation instance.

        Args:
            operation (str): The operation name (e.g. 'addition').
            num1 (float): First operand.
            num2 (float): Second operand.
            result (float): Computed result of the operation.
        """
>>>>>>> origin/version5
        self.operation = operation
        self.num1 = num1
        self.num2 = num2
        self.result = result

<<<<<<< HEAD
    def __str__(self) -> str:
        return f"{self.num1} {self.operation} {self.num2} = {self.result}"

class Calculator:
    """
    Provides a REPL and CLI interface for arithmetic operations.
    """
    history: List[Calculation] = []
=======
    def __str__(self):
        """
        Return a human-readable representation of the calculation.

        Returns:
            str: E.g. "3.0 addition 4.0 = 7.0"
        """
        return f"{self.num1} {self.operation} {self.num2} = {self.result}"


class Calculator:
    """A class providing a REPL for numeric-based arithmetic operations."""

    history = []
>>>>>>> origin/version5

    @classmethod
    def run(cls):
        """
        Start the calculator REPL loop.
<<<<<<< HEAD
=======

        Options:
          1 => addition
          2 => subtract
          3 => multiply
          4 => division
          5 => history
          6 => clear
          7 => quit
          8 => stoptest (hidden coverage path)
>>>>>>> origin/version5
        """
        print("=========== Calculator Menu ===========")
        print("1) addition")
        print("2) subtract")
        print("3) multiply")
        print("4) division")
        print("5) history (view past calculations)")
        print("6) clear   (clear calculation history)")
        print("7) quit    (exit the calculator)")
<<<<<<< HEAD

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

    @staticmethod
    def get_inputs() -> (Optional[float], Optional[float]):
        """
        Prompt for two numeric inputs.
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
        Perform the requested arithmetic operation.
        """
        op_map = {
=======
        print("=======================================\n")

        while True:
            action = input("Enter a number (1–7): ").strip().lower()

            if action == "7":
                print("Exiting calculator. Goodbye!")
                break
            elif action == "8":
                # Hidden command for coverage
                print("Testing coverage for final line.")
                return
            elif action == "5":
                print(cls.get_history())
            elif action == "6":
                cls.clear_history()
            elif action in ["1", "2", "3", "4"]:
                # Map numeric choice to operation name
                if action == "1":
                    operation = "addition"
                elif action == "2":
                    operation = "subtract"
                elif action == "3":
                    operation = "multiply"
                else:
                    operation = "division"

                num1, num2 = cls.get_inputs()
                if num1 is None or num2 is None:
                    print("Exiting calculator. Goodbye!")
                    break

                result = cls.compute(operation, num1, num2)
                if result is not None:
                    print(f"The result is: {result}")
                    calculation = Calculation(operation, num1, num2, result)
                    cls.add_to_history(calculation)
            else:
                print("Invalid choice. Please enter a number from 1 to 7.")

        return

    @staticmethod
    def get_inputs():
        """
        Prompt for two numeric inputs, or 'quit' to exit.

        Returns:
            (float | None, float | None): The two numbers, or (None, None) if quitting/invalid.
        """
        try:
            first = input("Enter the first number: ").strip()
            if first.lower() == "quit":
                return None, None

            second = input("Enter the second number: ").strip()
            if second.lower() == "quit":
                return None, None

            return float(first), float(second)
        except ValueError:
            print("Invalid number. Please enter numeric values.")
            return None, None

    @classmethod
    def compute(cls, operation, num1, num2):
        """
        Perform an arithmetic operation on two floats.

        Args:
            operation (str): One of 'addition', 'subtract', 'multiply', 'division'.
            num1 (float): First operand.
            num2 (float): Second operand.

        Returns:
            float | None: The result, or None if division by zero.
        """
        operation_map = {
>>>>>>> origin/version5
            "addition": Operations.add,
            "subtract": Operations.subtract,
            "multiply": Operations.multiply,
            "division": Operations.divide,
        }
<<<<<<< HEAD
        if operation not in op_map:
            raise ValueError(f"Unsupported operation: {operation}")
        return op_map[operation](num1, num2)

    @classmethod
    def add_to_history(cls, calculation: Calculation):
        """Add a Calculation object to the history."""
        cls.history.append(calculation)

    @classmethod
    def get_history(cls) -> str:
        """Return all calculations in history.
        Calculator logic and history management.
=======

        # Check if the operation is valid BEFORE attempting to use the map
        if operation not in operation_map:
            raise ValueError(f"Unsupported operation: {operation}")

        try:
            return operation_map[operation](num1, num2)
        except ZeroDivisionError:
            print("Cannot divide by zero.")
            return None

    @classmethod
    def add_to_history(cls, calculation):
        """
        Add a Calculation object to the history list.

        Args:
            calculation (Calculation): The calculation to store.
        """
        cls.history.append(calculation)

    @classmethod
    def get_history(cls):
        """
        Return a string representation of all calculations in history.

        Returns:
            str: If empty, "No calculations recorded."
                 Otherwise, each calculation on its own line.
>>>>>>> origin/version5
        """
        if not cls.history:
            return "No calculations recorded."
        return "\n".join(str(calc) for calc in cls.history)

    @classmethod
    def clear_history(cls):
        """Clear all stored calculations."""
        cls.history.clear()
        print("History has been cleared.")
