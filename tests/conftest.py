# Editor: ##@sb2853.njit.edu
import pytest
from faker import Faker
from decimal import Decimal
from app.calculator import Calculator

fake = Faker()


def pytest_addoption(parser):
    parser.addoption(
        "--num_records",
        action="store",
        default=10,
        type=int,
        help="Number of records to generate for property-based tests."
    )

@pytest.fixture(scope="session")
def num_records(request):
    return request.config.getoption("num_records")


@pytest.fixture(scope="session")
def faker():
    return Faker()


def pytest_generate_tests(metafunc):
    if (
        "num1" in metafunc.fixturenames and
        "num2" in metafunc.fixturenames and
        "operation" in metafunc.fixturenames and
        "expected_result" in metafunc.fixturenames
    ):
        from tests.test_utils import generate_test_data
        num_records = metafunc.config.getoption("num_records")
        test_cases = generate_test_data(num_records)
        metafunc.parametrize(
            ("num1", "num2", "operation", "expected_result"),
            test_cases
        )
