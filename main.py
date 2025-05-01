<<<<<<< HEAD
"""
Main entry point for the calculator CLI and REPL.
Editor: ##@sb2853.njit.edu
"""
"""
Handles CLI and REPL modes.
"""

import sys
from app.calculator import Calculator
=======
import sys
from app.calculator import Calculator
from decimal import Decimal, InvalidOperation


def calculation(value1, value2, operation):
    """
    Executes a mathematical operation using the Calculator class and prints the result.
    Handles input validation and error cases.
    """
    operation_map = {
        'add': 'addition',
        'subtract': 'subtract',
        'multiply': 'multiply',
        'divide': 'division'
    }

    try:
        num1, num2 = map(Decimal, [value1, value2])

        if operation == 'divide' and num2 == 0:
            print("An error occurred: Cannot divide by zero")
            return

        if operation in operation_map:
            actual_operation = operation_map[operation]
            outcome = Calculator.compute(actual_operation, float(num1), float(num2))
            print(f"The result of {num1} {operation} {num2} is equal to {int(outcome) if outcome.is_integer() else outcome}")
        else:
            print(f"Unknown operation: {operation}")

    except InvalidOperation:
        print(f"Invalid number input: {value1} or {value2} is not a valid number.")

>>>>>>> origin/version5

def cli_mode():
    """
    Handles command-line input for performing calculations.
    """
    if len(sys.argv) == 1:
        print("Starting REPL mode... Type 'quit' to exit.")
        Calculator.run()
        return

    if len(sys.argv) != 4:
        print("Usage: python main.py <num1> <num2> <operation>")
        sys.exit(1)

    _, val1, val2, op = sys.argv
<<<<<<< HEAD
    try:
        num1 = float(val1)
        num2 = float(val2)
    except ValueError:
        print("Invalid numeric input.")
        sys.exit(1)

    operation_map = {
        "add": "addition",
        "subtract": "subtract",
        "multiply": "multiply",
        "divide": "division"
    }
    operation = operation_map.get(op)
    if not operation:
        print(f"Unknown operation: {op}")
        sys.exit(1)

    try:
        result = Calculator.compute(operation, num1, num2)
        # Format numbers as int if possible, else float
        def fmt(val):
            return int(val) if val == int(val) else val
        print(f"The result of {fmt(num1)} {op} {fmt(num2)} is equal to {fmt(result)}")
    except ZeroDivisionError:
        print("Cannot divide by zero.")

if __name__ == '__main__':
=======
    calculation(val1, val2, op)


if __name__ == '__main__':  # pragma: no cover
>>>>>>> origin/version5
    cli_mode()
