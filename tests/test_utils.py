"""
Test utilities for property-based and parameterized tests.
"""
from decimal import Decimal
from app.calculator import Calculator
from faker import Faker


def generate_test_data(num_records=10, seed=None):
    """
    Generate test data for arithmetic operations using Calculator.compute().
    Args:
        num_records (int): Number of test records to generate.
        seed (int, optional): Seed for reproducibility.
    Returns:
        list of tuples: (num1, num2, operation, expected_result)
    """
    fake = Faker()
    if seed is not None:
        Faker.seed(seed)
    operations = ["addition", "subtract", "multiply", "division"]
    test_cases = []
    for _ in range(num_records):
        num1 = Decimal(fake.random_int(min=-100, max=100))
        num2 = Decimal(fake.random_int(min=-100, max=100))
        operation = fake.random_element(elements=operations)
        # Avoid division by zero input
        if operation == "division" and num2 == 0:
            num2 = Decimal(1)
        result = Calculator.compute(operation, float(num1), float(num2))
        test_cases.append((num1, num2, operation, result))
    return test_cases
