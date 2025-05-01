"""
Main entry point for the calculator CLI and REPL.
Editor: ##@sb2853.njit.edu
"""
"""
Handles CLI and REPL modes.
"""

import sys
from app.calculator import Calculator

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
    cli_mode()
