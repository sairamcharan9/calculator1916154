"""
Test utilities for property-based and parameterized tests.
"""
from decimal import Decimal
from src.calculator import Calculator
from faker import Faker
import random
import math


def generate_test_data(num_records=10, seed=None):
    """
    Generate test data for arithmetic operations.
    
    Args:
        num_records (int): Number of test records to generate.
        seed (int, optional): Seed for reproducibility.
        
    Returns:
        list of tuples: (num1, num2, operation, expected_result)
    """
    fake = Faker()
    if seed is not None:
        Faker.seed(seed)
        random.seed(seed)
    
    operations = ["add", "subtract", "multiply", "divide", "power"]
    test_cases = []
    
    for _ in range(num_records):
        # Generate random numbers with reasonable ranges
        num1 = fake.pyfloat(min_value=-100, max_value=100, right_digits=2)
        num2 = fake.pyfloat(min_value=-100, max_value=100, right_digits=2)
        
        # Choose random operation
        operation = fake.random_element(elements=operations)
        
        # Handle special cases
        if operation == "divide" and abs(num2) < 0.001:
            num2 = 1.0  # Avoid division by zero
        
        if operation == "power":
            # Limit exponent to avoid huge numbers
            num2 = min(max(num2, -5), 5)
        
        # Calculate expected result (skip invalid math domains)
        try:
            if operation == "add":
                expected_result = num1 + num2
            elif operation == "subtract":
                expected_result = num1 - num2
            elif operation == "multiply":
                expected_result = num1 * num2
            elif operation == "divide":
                expected_result = num1 / num2
            elif operation == "power":
                expected_result = math.pow(num1, num2)
        except (ValueError, ZeroDivisionError, OverflowError):
            continue  # skip invalid test case
        test_cases.append((num1, num2, operation, expected_result))
    
    return test_cases
