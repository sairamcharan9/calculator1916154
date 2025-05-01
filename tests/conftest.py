<<<<<<< HEAD
# Editor: ##@sb2853.njit.edu
=======
>>>>>>> origin/version5
import pytest
from faker import Faker
from decimal import Decimal
from app.calculator import Calculator

fake = Faker()

<<<<<<< HEAD
def pytest_addoption(parser):
=======

def generate_test_data(num_records):
    """Generate test data for arithmetic operations using Calculator.compute()."""
    operations = ["addition", "subtract", "multiply", "division"]
    test_cases = []

    for _ in range(num_records):
        num1 = Decimal(fake.random_int(min=-100, max=100))
        num2 = Decimal(fake.random_int(min=-100, max=100))
        operation = fake.random_element(elements=operations)

        # Avoid division by zero input
        if operation == "division" and num2 == 0:
            num2 = Decimal(1)

        # Compute expected result using actual production logic
        result = Calculator.compute(operation, float(num1), float(num2))

        test_cases.append((num1, num2, operation, result))

    return test_cases


def pytest_addoption(parser):
    """Add CLI option to control the number of test records."""
>>>>>>> origin/version5
    parser.addoption(
        "--num_records",
        action="store",
        default=10,
        type=int,
        help="Number of test records to generate",
    )

<<<<<<< HEAD
def generate_test_data(num_records):
    operations = ["addition", "subtract", "multiply", "division"]
    test_cases = []
    for _ in range(num_records):
        num1 = Decimal(fake.random_int(min=-100, max=100))
        num2 = Decimal(fake.random_int(min=-100, max=100))
        operation = fake.random_element(elements=operations)
        if operation == "division" and num2 == 0:
            num2 = Decimal(1)
        result = Calculator.compute(operation, float(num1), float(num2))
        test_cases.append((num1, num2, operation, result))
    return test_cases

def pytest_generate_tests(metafunc):
=======

def pytest_generate_tests(metafunc):
    """Dynamically parameterize tests requiring (num1, num2, operation, expected_result)."""
>>>>>>> origin/version5
    if {"num1", "num2", "operation", "expected_result"}.issubset(set(metafunc.fixturenames)):
        num_records = metafunc.config.getoption("num_records")
        test_data = generate_test_data(num_records)
        metafunc.parametrize("num1,num2,operation,expected_result", test_data)
<<<<<<< HEAD

@pytest.fixture(scope="session")
def faker():
    return Faker()
=======
>>>>>>> origin/version5
