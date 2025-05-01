# Editor: ##@sb2853.njit.edu
import pytest
from faker import Faker
from decimal import Decimal
from app.calculator import Calculator

fake = Faker()



@pytest.fixture(scope="session")
def faker():
    return Faker()
