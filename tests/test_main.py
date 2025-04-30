# test_main.py for testing main.py
# Copying from calc_app for full test coverage
import sys
import pytest
from calculator import Calculator
from decimal import Decimal

# Example test for main.py functionality
# Add more tests as in calc_app/test_main.py if needed

def test_addition(capsys):
    sys.argv = ["main.py", "2", "3", "add"]
    from main import main
    main()
    captured = capsys.readouterr()
    assert "The result of 2 add 3 is equal to 5" in captured.out
