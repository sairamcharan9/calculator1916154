# Calculator Project 

![Python Version](https://img.shields.io/badge/python-3.13%2B-blue)
![Tests](https://img.shields.io/badge/tests-34%20passed-success)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)

## Student Information
🎓 **Name**: Sai Ram Charan  
🔖 **ID**: 1916154  
📅 **Last Updated**: 2025-04-30

## Project Overview
A robust command-line calculator with:
- 🧮 Basic arithmetic operations (+, -, ×, ÷)
- 🔢 Decimal precision handling
- 🛡️ Comprehensive error checking
- ✅ 100% test coverage
- 🔄 Property-based testing with Faker

## Features
```text
✔️ CLI interface with argument parsing
✔️ Precise decimal arithmetic
✔️ Input validation and error handling:
   - Invalid numeric inputs
   - Division by zero
   - Unknown operations
✔️ Automated testing framework
✔️ PEP8 compliant codebase
```

## Quick Start

### Run the Calculator
```bash
python main.py
```

### Run All Tests
```bash
pytest tests
```

### Property-Based Testing with Faker
To run property-based tests with a custom number of random cases (using Faker):
```bash
pytest tests --num_records=100
```
This will dynamically generate 100 random test cases for the calculator using Faker.

For full debug output:
```bash
pytest tests --num_records=10 -v -s
```

## Installation
```bash
pip install -r requirements.txt
```

## Usage
```bash
python main.py <num1> <num2> <operation>

# Example:
python main.py 15.5 3.2 add
# Output: The result of 15.5 add 3.2 is equal to 18.7
```

## Testing & Coverage

This project is fully tested and achieves 99% code coverage (1 uncovered line in tests/conftest.py). All 54 tests pass, including:
- Unit tests for calculator logic and operations
- Integration tests for CLI and REPL workflows
- Property-based tests with random data (using Faker)

Example test summary:
```
============================= 54 passed in 0.17s =============================
---------- coverage: platform win32, python 3.13.3-final-0 -----------
Name                                 Stmts   Miss  Cover   Missing
------------------------------------------------------------------
app\__init__.py                          0      0   100%
app\calculator\__init__.py              88      0   100%
app\operations\__init__.py              15      0   100%
main.py                                 27      0   100%
tests\__init__.py                        0      0   100%
tests\conftest.py                       24      1    96%   21
tests\test_calculator.py                87      0   100%
tests\test_generated_operations.py       4      0   100%
tests\test_main.py                      30      0   100%
tests\test_operations.py                17      0   100%
------------------------------------------------------------------
TOTAL                                  292      1    99%
```

---

## Creative Features & Enhancements

- **Hidden Command**: A secret `stoptest` command exists in the REPL for test coverage.
- **Calculation History**: View and clear calculation history interactively.
- **Robust CLI**: Supports both CLI and REPL modes with strong input validation.
- **Property-Based Testing**: Uses Faker to generate random test cases for reliability.
- **PEP8 Compliance**: Clean, maintainable, and modular code.
- **100% Pass Rate**: All tests pass with high coverage.

### Creative Suggestions for Future Enhancement
- Add colorized CLI output for better user experience (using `colorama` or similar).
- Implement command auto-completion and input suggestions in REPL.
- Support for advanced operations (power, modulus, square root, etc).
- Add a persistent history feature (save/load to file).
- Provide a web or GUI frontend for the calculator.
- Add user profiles and personalized settings.

---

**NOTE:** If you face any difficulties please contact me at <code> sb2853@njit.edu </code>


