"""
Configuration and fixtures for pytest.
"""
import os
import pytest
import random
from faker import Faker
import tempfile
import pandas as pd

def pytest_addoption(parser):
    """Add command-line options to pytest."""
    parser.addoption(
        "--num_records",
        action="store",
        default=10,
        type=int,
        help="Number of random records to generate for tests"
    )

@pytest.fixture(scope="session")
def num_records(request):
    """Get the number of records to generate from command line."""
    return request.config.getoption("--num_records")

@pytest.fixture(scope="session")
def faker():
    """Create a Faker instance with a fixed seed for reproducibility."""
    random.seed(42)  # Set seed for reproducibility
    fake = Faker()
    Faker.seed(42)
    return fake

@pytest.fixture
def temp_data_dir(tmpdir):
    """Create a temporary data directory for testing."""
    data_dir = tmpdir.mkdir("data")
    return str(data_dir)

@pytest.fixture
def temp_history_file(tmpdir):
    """Create a temporary history file for testing."""
    history_file = tmpdir.join("history.csv")
    return str(history_file)

@pytest.fixture
def temp_log_file(tmpdir):
    """Create a temporary log file for testing."""
    log_file = tmpdir.join("log.txt")
    return str(log_file)

@pytest.fixture
def csv_data_for_tests(temp_data_dir, faker, num_records):
    """Generate test CSV data."""
    # Create CSV files for testing
    states_data = []
    for _ in range(num_records):
        states_data.append({
            'Abbreviation': faker.state_abbr(),
            'State': faker.state(),
            'Population': faker.random_int(min=10000, max=40000000)
        })
    
    states_df = pd.DataFrame(states_data)
    csv_path = os.path.join(temp_data_dir, "states.csv")
    states_df.to_csv(csv_path, index=False)
    
    return {
        'dir': temp_data_dir,
        'files': {
            'states': csv_path
        },
        'dataframes': {
            'states': states_df
        }
    }

def pytest_generate_tests(metafunc):
    """Generate parameterized tests."""
    # For arithmetic operation tests
    if ("num1" in metafunc.fixturenames and 
        "num2" in metafunc.fixturenames and 
        "operation" in metafunc.fixturenames and 
        "expected_result" in metafunc.fixturenames):
        
        from tests.test_utils import generate_test_data
        num_records = metafunc.config.getoption("--num_records")
        test_cases = generate_test_data(num_records, seed=42)
        metafunc.parametrize(
            ("num1", "num2", "operation", "expected_result"),
            test_cases
        )
