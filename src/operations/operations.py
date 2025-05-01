import math
import statistics

class Operations:
    """All core, scientific, and statistical calculator operations."""

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
        Raises:
            ZeroDivisionError: If y == 0.
        """
        if y == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return x / y

    @staticmethod
    def modulus(x: float, y: float) -> float:
        """Return the modulus of x and y. Raises ZeroDivisionError if y is zero."""
        if y == 0:
            raise ZeroDivisionError("Cannot modulo by zero.")
        return x % y

    @staticmethod
    def exponentiate(x: float, y: float) -> float:
        """Return x raised to the power of y."""
        return x ** y

    @staticmethod
    def sqrt(x: float) -> float:
        """Return the square root of x. Raises ValueError if x < 0."""
        if x < 0:
            raise ValueError("Cannot take square root of negative number.")
        return math.sqrt(x)

    @staticmethod
    def absolute(x: float) -> float:
        """Return the absolute value of x."""
        return abs(x)

    @staticmethod
    def negate(x: float) -> float:
        """Return the negation of x."""
        return -x

    @staticmethod
    def reciprocal(x: float) -> float:
        """Return the reciprocal of x. Raises ZeroDivisionError if x == 0."""
        if x == 0:
            raise ZeroDivisionError("Cannot take reciprocal of zero.")
        return 1 / x

    @staticmethod
    def sin(x: float) -> float:
        """Return the sine of x (radians)."""
        return math.sin(x)

    @staticmethod
    def cos(x: float) -> float:
        """Return the cosine of x (radians)."""
        return math.cos(x)

    @staticmethod
    def tan(x: float) -> float:
        """Return the tangent of x (radians)."""
        return math.tan(x)

    @staticmethod
    def log10(x: float) -> float:
        """Return the base-10 logarithm of x. Raises ValueError if x <= 0."""
        if x <= 0:
            raise ValueError("Math domain error: log10 undefined for x <= 0.")
        return math.log10(x)

    @staticmethod
    def ln(x: float) -> float:
        """Return the natural logarithm of x. Raises ValueError if x <= 0."""
        if x <= 0:
            raise ValueError("Math domain error: ln undefined for x <= 0.")
        return math.log(x)

    @staticmethod
    def exp(x: float) -> float:
        """Return e raised to the power of x."""
        return math.exp(x)

    @staticmethod
    def factorial(x: float) -> int:
        """Return the factorial of x. Raises ValueError if x is negative or not integer."""
        if x < 0 or int(x) != x:
            raise ValueError("Factorial only defined for non-negative integers.")
        return math.factorial(int(x))

    @staticmethod
    def floor(x: float) -> int:
        """Return the floor of x."""
        return math.floor(x)

    @staticmethod
    def ceil(x: float) -> int:
        """Return the ceiling of x."""
        return math.ceil(x)

    @staticmethod
    def round(x: float, ndigits: int = 0) -> float:
        """Return x rounded to ndigits decimal places."""
        return round(x, ndigits)

    @staticmethod
    def percent(x: float, y: float) -> float:
        """Return what percent x is of y. Raises ZeroDivisionError if y == 0."""
        if y == 0:
            raise ZeroDivisionError("Cannot calculate percent with denominator zero.")
        return (x / y) * 100

    @staticmethod
    def mean(nums):
        """Return the mean of nums."""
        return statistics.mean(nums)

    @staticmethod
    def median(nums):
        """Return the median of nums."""
        return statistics.median(nums)

    @staticmethod
    def mode(nums):
        """Return the mode of nums."""
        return statistics.mode(nums)

    @staticmethod
    def variance(nums):
        """Return the variance of nums."""
        return statistics.variance(nums)

    @staticmethod
    def stdev(nums):
        """Return the standard deviation of nums."""
        return statistics.stdev(nums)

    @staticmethod
    def minimum(nums):
        """Return the minimum value in nums."""
        return min(nums)

    @staticmethod
    def maximum(nums):
        """Return the maximum value in nums."""
        return max(nums)

    @staticmethod
    def total(nums):
        """Return the sum of nums."""
        return sum(nums)

    @staticmethod
    def count(nums):
        """Return the count of nums."""
        return len(nums)
