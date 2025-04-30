import pytest
from faker import Faker
import random

# Add command-line option for number of records

def pytest_addoption(parser):
    parser.addoption(
        "--num_records",
        action="store",
        default=10,
        type=int,
        help="Number of random calculation records to generate for tests."
    )

@pytest.fixture(scope="session")
def faker():
    return Faker()

@pytest.fixture(scope="session")
def num_records(request):
    return int(request.config.getoption("--num_records"))

@pytest.fixture(scope="session")
def random_calculations(faker, num_records):
    operations = ['add', 'subtract', 'multiply', 'divide']
    data = []
    for _ in range(num_records):
        a = faker.random_int(min=1, max=100)
        b = faker.random_int(min=1, max=100)
        op = random.choice(operations)
        # Avoid division by zero
        if op == 'divide' and b == 0:
            b = faker.random_int(min=1, max=100)
        if op == 'add':
            expected = a + b
        elif op == 'subtract':
            expected = a - b
        elif op == 'multiply':
            expected = a * b
        elif op == 'divide':
            expected = a / b
        data.append((a, b, op, expected))
    return data
