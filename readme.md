# Homework3
## Name : SAI RAM CHARAN
## ID : 1916154
## App:CALCULATOR-homework-4

## Test Results (2025-04-30)

**Test Command:**
```bash
pytest --num_records=100
```

**Output Summary:**
```text
================================================ test session starts =================================================
platform win32 -- Python 3.13.3, pytest-8.0.0, pluggy-1.4.0
collected 34 items

tests/test_calculation.py ....................                                                                 [100%]
tests/test_calculations.py ...............                                                                    [100%]
tests/test_calculator.py ........                                                                             [100%] 
tests/test_faker_calculations.py .                                                                           [100%]
tests/test_main.py ..............                                                                           [100%]
tests/test_operations.py .........                                                                          [100%]

================================================= 34 passed in 0.21s =================================================
```

**Key Features Verified:**
- ✅ All 34 tests passed successfully
- 🔄 Parameterized testing with 100 records using Faker
- 🛠️ Core calculator operations (add/subtract/multiply/divide)
- 🚫 Error handling for division by zero
- 📚 History tracking functionality
- 📊 Data-driven testing patterns

**Dependencies Used:**
- Faker==23.1.0
- pytest==8.0.0
- coverage==7.4.1
