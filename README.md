# Advanced Python Calculator – Midterm Project

Welcome to the Advanced Python Calculator, a professional, extensible, and fully-tested command-line application designed to showcase modern software engineering best practices. This project is the culmination of the midterm assignment and demonstrates:

- Clean, modular Python code following PEP 8 guidelines
- Multiple design patterns (Command, Facade, Factory, Singleton, Strategy)
- Dynamic plugin architecture for easy extension
- Robust logging and configuration via environment variables
- Pandas-powered calculation history with CSV persistence
- Comprehensive testing and continuous integration

## Key Features

- **Interactive REPL:** Perform calculations and manage history in a user- friendly shell.
- **Plugin System:** Dynamically load new commands without changing core code.
- **Calculation History:** View, save, load, and clear your calculation history (powered by Pandas).
- **Professional Logging:** All operations are logged with configurable levels and outputs.
- **Design Patterns:** Architecture leverages Command, Facade, Factory, Singleton, and Strategy patterns for maintainability and scalability.
- **Data Processing:** Process CSV files using the Pandas-based DataFacade for advanced data manipulation.
- **Tested & CI-Ready:** Achieves 90%+ coverage and passes all tests in GitHub Actions.

## Command-Line Interface (CLI) Usage

The calculator is primarily used via a modern, interactive CLI (REPL). To start the CLI, run:

```sh
python main.py
```

## Example CLI Session (as seen when running `python main.py`)
```
┌───────────────────────────────────────────────────────┐
│ Calculator Commands                                    │
├───────────────────────────────────────────────────────┤
│ 1.  add <num1> <num2>     │ 6.  sqrt <num>            │
│ 2.  subtract <num1> <num2>│ 7.  exp <num>             │
│ 3.  multiply <num1> <num2>│ 8.  log <num>             │
│ 4.  divide <num1> <num2>  │ 9.  logbase <num> <base>  │
│ 5.  power <num1> <num2>   │ 10. abs <num>             │
├───────────────────────────────────────────────────────┤
│ Statistical Commands                                   │
├───────────────────────────────────────────────────────┤
│ 11. max <nums...>         │ 14. median <nums...>      │
│ 12. min <nums...>         │ 15. mode <nums...>        │
│ 13. mean <nums...>        │ 16. stdev <nums...>       │
├───────────────────────────────────────────────────────┤
│ History & Data Commands                                │
├───────────────────────────────────────────────────────┤
│ 17. history               │ 20. save_history         │
│ 18. clear_history         │ 21. load_history         │
│ 19. undo                  │ 22. redo                 │
├───────────────────────────────────────────────────────┤
│ Data Processing Commands                               │
├───────────────────────────────────────────────────────┤
│ 23. list_csv              │ 25. data_info             │
│ 24. load_csv <filename>   │ 26. filter_data <col> <val> [op]│
│                           │ 27. save_csv [filename]   │
├───────────────────────────────────────────────────────┤
│ Other Commands                                         │
├───────────────────────────────────────────────────────┤
│ 28. help                  │ 29. exit                  │

========================================
   Advanced Python Calculator (CLI)
   Type 'menu' or 'help' for options
   Type 'exit' to quit
========================================

Enter command (or 'menu', 'help', 'exit'): add
Enter two numbers (comma or space separated): 5 7
RESULT: 12.0

Enter command (or 'menu', 'help', 'exit'): mean
Enter numbers (comma or space separated): 1, 2, 3, 4
RESULT: 2.5

Enter command (or 'menu', 'help', 'exit'): history
1 add 2 = 3
5 add 7 = 12
mean 1,2,3,4 = 2.5

Enter command (or 'menu', 'help', 'exit'): exit
Goodbye!

### CLI Workflow
- **Prompt:** The CLI prompts you for a command (e.g., `add`, `subtract`, `mean`, `load_csv`, etc.).
- **Arguments:** After entering a command, you are prompted for the required arguments (numbers, filenames, etc.).
- **Result:** The result is displayed and saved to history.
- **History:** All commands and results are logged and can be viewed, saved, loaded, or cleared.
- **Error Handling:** Invalid commands or arguments are handled gracefully with clear error messages.

#### Example Session
```
Enter command (or 'menu', 'help', 'exit'): add
Enter two numbers (comma or space separated): 5, 7
RESULT: 12.0

Enter command (or 'menu', 'help', 'exit'): mean
Enter numbers (comma or space separated): 1, 2, 3, 4
RESULT: 2.5

Enter command (or 'menu', 'help', 'exit'): history
1 add 2 = 3
5 add 7 = 12
mean 1,2,3,4 = 2.5
```

### Supported Commands
- **Arithmetic:** `add`, `subtract`, `multiply`, `divide`, `power`, `modulus`
- **Scientific:** `sqrt`, `exp`, `log`, `logbase`, `abs`, `factorial`
- **Statistics:** `mean`, `median`, `mode`, `stdev`, `max`, `min`
- **History:** `history`, `clear_history`, `save_history`, `load_history`, `undo`, `redo`
- **Data/CSV:** `load_csv`, `save_csv`, `filter_data`, `list_csv`, `data_info`
- **Help/Menu:** `menu`, `help`, `exit`

### Plugin System
- New commands can be added as plugins in the `src/plugins/` directory and will be auto-discovered at runtime.

## Design Patterns Implementation

### Command Pattern
The calculator uses the Command pattern to encapsulate operations as objects, allowing for:
- Easy addition of new operations
- Uniform interface for all calculator functions
- Support for operation history, undo/redo functionality

**Implementation:** [src/commands/command_base.py](src/commands/command_base.py) defines the abstract Command interface, with concrete implementations in [src/commands/arithmetic_commands.py](src/commands/arithmetic_commands.py).

### Facade Pattern
The Pandas integration uses the Facade pattern to simplify the complex DataFrame API:
- Provides a clean, simple interface for history management and CSV processing
- Hides the complexity of Pandas operations
- Makes the codebase more maintainable

**Implementation:** 
- [src/history/data_manager.py](src/history/data_manager.py) implements the Facade pattern for history operations
- [src/plugins/data/__init__.py](src/plugins/data/__init__.py) implements the Facade pattern for CSV data processing

### Singleton Pattern
The logger configuration uses the Singleton pattern to ensure:
- Only one logger instance exists throughout the application
- Consistent logging configuration
- Resource efficiency

**Implementation:** [src/history/logger.py](src/history/logger.py) implements the Singleton pattern for logger configuration.

### Factory Method Pattern
The plugin system uses the Factory pattern to:
- Dynamically create command instances
- Decouple command creation from execution
- Support runtime extension

**Implementation:** [src/plugins/__init__.py](src/plugins/__init__.py) implements the Factory pattern for command creation.

## CSV Data Processing

The calculator includes a powerful data processing feature that allows you to work with CSV files:

### Available Commands

- `list_csv`: Lists all available CSV files in the data directory
- `load_csv`: Loads a CSV file into memory
- `data_info`: Displays information about the current DataFrame
- `filter_data`: Filters the DataFrame based on a column and value
- `save_csv`: Saves the current DataFrame to a CSV file

### Example Usage

```
> list_csv
Available CSV files:
1. states.csv
2. gpt_states.csv

> load_csv states.csv
Successfully loaded states.csv with 6 rows and 2 columns.

> data_info
File: states.csv
Rows: 6
Columns: Abbreviation, State

> filter_data State California
DataFrame filtered on State == California. 1 rows remaining.

> save_csv filtered_states.csv
DataFrame saved to filtered_states.csv.
```

The CSV processing feature demonstrates the Facade design pattern, providing a simplified interface to the complex Pandas library.

## Environment Variables

The calculator uses environment variables for dynamic configuration:
- `LOG_LEVEL`: Sets the logging level (DEBUG, INFO, WARNING, ERROR)
- `LOG_FILE`: Path to the log file
- `ENVIRONMENT`: Current environment (development, testing, production)
- `DEBUG`: Enable/disable debug mode
- `HISTORY_FILE`: Path to the history CSV file

**Implementation:** [src/history/logger.py](src/history/logger.py) and [src/history/data_manager.py](src/history/data_manager.py) use environment variables for configuration.

## Logging System

The calculator implements a comprehensive logging system:
- Multiple log levels (DEBUG, INFO, WARNING, ERROR)
- File and console output
- Configurable via environment variables
- Detailed operation tracking

**Implementation:** [src/history/logger.py](src/history/logger.py) provides the logging infrastructure used throughout the application.

## Exception Handling

The calculator demonstrates both error handling paradigms:

### Look Before You Leap (LBYL)
- Checks conditions before performing operations
- Prevents errors from occurring

**Example:** [src/commands/arithmetic_commands.py](src/commands/arithmetic_commands.py) checks for division by zero before performing division.

### Easier to Ask for Forgiveness than Permission (EAFP)
- Uses try/except blocks to handle errors
- More Pythonic approach

**Example:** [src/plugins/__init__.py](src/plugins/__init__.py) uses try/except for plugin loading and command execution.

## Getting Started

1. **Clone the repository and create a virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Unix/MacOS
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment:**
   - Copy `.env.example` to `.env` and adjust as needed.

4. **Run the calculator:**
   ```bash
   python main.py
   ```

5. **Run tests:**
   ```bash
   pytest --cov
   ```

## Project Structure

```
midterm-calculator/
├── logs/                  # Log files directory
├── src/                   # Source code
│   ├── calculator/        # Core calculator functionality
│   ├── commands/          # Command pattern implementation
│   ├── history/           # History management with Pandas
│   │   └── data/          # CSV history storage
│   ├── operations/        # Basic arithmetic operations
│   └── plugins/           # Dynamic plugin system
├── tests/                 # Test suite
├── .env.example           # Environment variable template
├── .gitignore             # Git ignore file
├── main.py                # Entry point
├── pytest.ini             # Pytest configuration
├── README.md              # This file
└── requirements.txt       # Dependencies
```

## Professional Practices
- **Version Control:** Using Git with frequent, meaningful commits
- **Testing:** Comprehensive test suite with pytest
- **Code Quality:** Adherence to PEP 8 standards with pylint
- **Documentation:** Detailed docstrings and README
- **CI/CD:** Automated testing with GitHub Actions

## Video Demonstration

[Link to video demonstration](https://youtu.be/your-video-id)

---

For details on architecture, design patterns, and future enhancements, see the inline code comments.
