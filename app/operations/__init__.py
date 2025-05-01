"""
Module: operations
Provides basic arithmetic operations for the calculator.
Editor: ##@sb2853.njit.edu
"""

class Operations:
    """Static methods for arithmetic operations."""

    @staticmethod
    def add(x: float, y: float) -> float:
        """Return the sum of x and y."""
        return x + y

    @staticmethod
    def subtract(x: float, y: float) -> float:
        """Return the difference of x and y."""
        return x - y

    @staticmethod
    def multiply(x: float, y: float) -> float:
        """Return the product of x and y."""
        return x * y

    @staticmethod
    def divide(x: float, y: float) -> float:
        """
        Return the quotient of x and y.
        Raises ZeroDivisionError if y == 0.
        """
        if y == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return x / y
