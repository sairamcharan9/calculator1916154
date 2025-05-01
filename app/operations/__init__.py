<<<<<<< HEAD
"""
Module: operations
Provides basic arithmetic operations for the calculator.
Editor: ##@sb2853.njit.edu
"""

class Operations:
    """Static methods for arithmetic operations."""

    @staticmethod
    def add(x: float, y: float) -> float:
=======
"""Arithmetic operations for the numeric-based calculator."""

class Operations:
    """Provides static methods for basic arithmetic."""

    @staticmethod
    def add(x, y):
>>>>>>> origin/version5
        """Return the sum of x and y."""
        return x + y

    @staticmethod
<<<<<<< HEAD
    def subtract(x: float, y: float) -> float:
=======
    def subtract(x, y):
>>>>>>> origin/version5
        """Return the difference of x and y."""
        return x - y

    @staticmethod
<<<<<<< HEAD
    def multiply(x: float, y: float) -> float:
=======
    def multiply(x, y):
>>>>>>> origin/version5
        """Return the product of x and y."""
        return x * y

    @staticmethod
<<<<<<< HEAD
    def divide(x: float, y: float) -> float:
        """
        Return the quotient of x and y.
        Raises ZeroDivisionError if y == 0.
=======
    def divide(x, y):
        """
        Return x / y, raising ZeroDivisionError if y == 0.

        Raises:
            ZeroDivisionError: If y == 0.
>>>>>>> origin/version5
        """
        if y == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return x / y
