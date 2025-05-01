"""
Main entry point for the Advanced Calculator application.
Handles CLI arguments and REPL mode.
"""

import os
import sys
import logging
from dotenv import load_dotenv
from src.calculator import Calculator
from src.history.logger import get_logger
from src.history.data_manager import history_manager
from src.plugins import discover_plugins, get_available_commands, execute_command

# Load environment variables
load_dotenv()

# Get logger
logger = get_logger('main')

# Environment info
environment = os.getenv('ENVIRONMENT', 'development')
debug_mode = os.getenv('DEBUG', 'False').lower() == 'true'

def display_welcome():
    """Display welcome message and environment info."""
    print("\n" + "=" * 60)
    print(f"{'ADVANCED CALCULATOR - SOFTWARE ENGINEERING EDITION':^60}")
    print("=" * 60)
    print(f"{'Environment:':<15} {environment}")
    print(f"{'Debug mode:':<15} {debug_mode}")
    print(f"{'Date & Time:':<15} {get_formatted_datetime()}")
    print("=" * 60)
    print("Type the number of a command or use 'help' for assistance.")
    print("=" * 60)

def get_formatted_datetime():
    """Return formatted date and time."""
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def display_menu(commands=None):
    """Display a numbered menu of available commands."""
    if commands is None:
        commands = get_available_commands()
    
    # Menu categories with box-drawing characters
    print("\n┌───────────────────────────────────────────────────────┐")
    print("│ Calculator Commands                                    │")
    print("├───────────────────────────────────────────────────────┤")
    print("│ 1.  add <num1> <num2>     │ 6.  sqrt <num>            │")
    print("│ 2.  subtract <num1> <num2>│ 7.  exp <num>             │")
    print("│ 3.  multiply <num1> <num2>│ 8.  log <num>             │")
    print("│ 4.  divide <num1> <num2>  │ 9.  logbase <num> <base>  │")
    print("│ 5.  power <num1> <num2>   │ 10. abs <num>             │")
    print("├───────────────────────────────────────────────────────┤")
    print("│ Statistical Commands                                   │")
    print("├───────────────────────────────────────────────────────┤")
    print("│ 11. max <nums...>         │ 14. median <nums...>      │")
    print("│ 12. min <nums...>         │ 15. mode <nums...>        │")
    print("│ 13. mean <nums...>        │ 16. stdev <nums...>       │")
    print("├───────────────────────────────────────────────────────┤")
    print("│ Memory & History Commands                              │")
    print("├───────────────────────────────────────────────────────┤")
    print("│ 17. undo                  │ 20. history               │")
    print("│ 18. redo                  │ 21. clear_history         │")
    print("│ 19. memory                │                           │")
    print("├───────────────────────────────────────────────────────┤")
    print("│ Data Processing Commands                               │")
    print("├───────────────────────────────────────────────────────┤")
    print("│ 22. list_csv              │ 24. data_info             │")
    print("│ 23. load_csv <filename>   │ 25. filter_data <col> <val> [op]│")
    print("│                           │ 26. save_csv [filename]   │")
    print("├───────────────────────────────────────────────────────┤")
    print("│ Other Commands                                         │")
    print("├───────────────────────────────────────────────────────┤")
    print("│ 27. help                  │ 28. exit                  │")
    print("└───────────────────────────────────────────────────────┘")

def handle_command(calculator, command_registry, command):
    """Process user command and execute appropriate action."""
    # Handle empty commands
    if not command.strip():
        return ""
    
    # Check if command is a number
    command_parts = command.split()
    if command_parts[0].isdigit():
        # Map number to actual command
        command_num = int(command_parts[0])
        if command_num == 1:
            command_parts[0] = "add"
        elif command_num == 2:
            command_parts[0] = "subtract"
        elif command_num == 3:
            command_parts[0] = "multiply"
        elif command_num == 4:
            command_parts[0] = "divide"
        elif command_num == 5:
            command_parts[0] = "power"
        elif command_num == 6:
            command_parts[0] = "sqrt"
        elif command_num == 7:
            command_parts[0] = "exp"
        elif command_num == 8:
            command_parts[0] = "log"
        elif command_num == 9:
            command_parts[0] = "logbase"
        elif command_num == 10:
            command_parts[0] = "abs"
        elif command_num == 11:
            command_parts[0] = "max"
        elif command_num == 12:
            command_parts[0] = "min"
        elif command_num == 13:
            command_parts[0] = "mean"
        elif command_num == 14:
            command_parts[0] = "median"
        elif command_num == 15:
            command_parts[0] = "mode"
        elif command_num == 16:
            command_parts[0] = "stdev"
        elif command_num == 17:
            command_parts[0] = "undo"
        elif command_num == 18:
            command_parts[0] = "redo"
        elif command_num == 19:
            command_parts[0] = "memory"
        elif command_num == 20:
            command_parts[0] = "history"
        elif command_num == 21:
            command_parts[0] = "clear_history"
        elif command_num == 22:
            command_parts[0] = "list_csv"
        elif command_num == 23:
            command_parts[0] = "load_csv"
        elif command_num == 24:
            command_parts[0] = "data_info"
        elif command_num == 25:
            command_parts[0] = "filter_data"
        elif command_num == 26:
            command_parts[0] = "save_csv"
        elif command_num == 27:
            command_parts[0] = "help"
        elif command_num == 28:
            command_parts[0] = "exit"
        
        # Reconstruct command
        command = ' '.join(command_parts)
    
    # Extract the command name and arguments
    parts = command.split()
    cmd_name = parts[0].lower()
    args = parts[1:]

    # Commands that require numeric input interactively if not given
    needs_numbers = {
        "add": 2, "subtract": 2, "multiply": 2, "divide": 2, "power": 2, "logbase": 2,
        "sqrt": 1, "exp": 1, "log": 1, "abs": 1,
        "max": -1, "min": -1, "mean": -1, "median": -1, "mode": -1, "stdev": -1
    }

    # Special commands
    if cmd_name == "exit":
        return "exit"
    elif cmd_name == "help":
        display_welcome()
        display_menu()
        return ""
    
    # If command requires numbers and none are given, prompt for them
    if cmd_name in needs_numbers:
        required = needs_numbers[cmd_name]
        if len(args) < (required if required > 0 else 1):
            prompt = (
                f"Enter {'two numbers' if required == 2 else 'one number' if required == 1 else 'numbers (space/comma separated)'}: "
            )
            nums_str = input(prompt)
            # Support both space and comma separation
            nums = [x for x in nums_str.replace(",", " ").split() if x.strip()]
            if not nums:
                return f"Error: {cmd_name} requires at least one numeric argument"
            if required > 0 and len(nums) < required:
                return f"Error: {cmd_name} requires {required} numeric argument(s)"
            args = nums
    
    if cmd_name in command_registry:
        cmd = command_registry[cmd_name]
        try:
            # Convert string arguments to the appropriate type
            if cmd_name in ["add", "subtract", "multiply", "divide", "power", "logbase"]:
                if len(args) < 2:
                    return f"Error: {cmd_name} requires two numeric arguments"
                result = cmd.execute(float(args[0]), float(args[1]))
                try:
                    history_manager.add_entry(cmd_name, args, result)
                except Exception as e:
                    logger.error(f"Failed to save history: {e}")
                return result
            elif cmd_name in ["sqrt", "exp", "log", "abs"]:
                if len(args) < 1:
                    return f"Error: {cmd_name} requires one numeric argument"
                result = cmd.execute(float(args[0]))
                try:
                    history_manager.add_entry(cmd_name, args, result)
                except Exception as e:
                    logger.error(f"Failed to save history: {e}")
                return result
            elif cmd_name in ["max", "min", "mean", "median", "mode", "stdev"]:
                if len(args) < 1:
                    return f"Error: {cmd_name} requires at least one numeric argument"
                result = cmd.execute(*[float(arg) for arg in args])
                try:
                    history_manager.add_entry(cmd_name, args, result)
                except Exception as e:
                    logger.error(f"Failed to save history: {e}")
                return result
            elif cmd_name in ["undo", "redo", "memory", "history", "clear_history"]:
                result = cmd.execute()
                try:
                    history_manager.add_entry(cmd_name, [], result)
                except Exception as e:
                    logger.error(f"Failed to save history: {e}")
                return result
            elif cmd_name == "list_csv":
                result = cmd.execute()
                try:
                    history_manager.add_entry(cmd_name, [], result)
                except Exception as e:
                    logger.error(f"Failed to save history: {e}")
                return result
            elif cmd_name == "load_csv":
                if len(args) < 1:
                    return "Error: load_csv requires a filename argument"
                result = cmd.execute(args[0])
                try:
                    history_manager.add_entry(cmd_name, args, result)
                except Exception as e:
                    logger.error(f"Failed to save history: {e}")
                return result
            elif cmd_name == "data_info":
                result = cmd.execute()
                try:
                    history_manager.add_entry(cmd_name, [], result)
                except Exception as e:
                    logger.error(f"Failed to save history: {e}")
                return result
            elif cmd_name == "filter_data":
                if len(args) < 2:
                    return "Error: filter_data requires column and value arguments"
                if len(args) > 2:
                    result = cmd.execute(args[0], args[1], args[2])
                    try:
                        history_manager.add_entry(cmd_name, args, result)
                    except Exception as e:
                        logger.error(f"Failed to save history: {e}")
                else:
                    result = cmd.execute(args[0], args[1])
                    try:
                        history_manager.add_entry(cmd_name, args, result)
                    except Exception as e:
                        logger.error(f"Failed to save history: {e}")
                return result
            elif cmd_name == "save_csv":
                if len(args) > 0:
                    result = cmd.execute(args[0])
                    try:
                        history_manager.add_entry(cmd_name, args, result)
                    except Exception as e:
                        logger.error(f"Failed to save history: {e}")
                else:
                    result = cmd.execute()
                    try:
                        history_manager.add_entry(cmd_name, [], result)
                    except Exception as e:
                        logger.error(f"Failed to save history: {e}")
                return result
            else:
                result = cmd.execute(*args)
                try:
                    history_manager.add_entry(cmd_name, args, result)
                except Exception as e:
                    logger.error(f"Failed to save history: {e}")
                return result
        except ValueError as e:
            logger.error(f"Value error in command {cmd_name}: {e}")
            return f"Error: {e}"
        except Exception as e:
            logger.error(f"Error in command {cmd_name}: {e}")
            return f"Error: {e}"
    else:
        return f"Unknown command: {cmd_name}"

def handle_cli_args():
    """
    Handle command-line arguments for direct calculation.
    Format: main.py <num1> <num2> <operation>
    """
    if len(sys.argv) != 4:
        print("Usage: python main.py <num1> <num2> <operation>")
        sys.exit(1)
    
    try:
        num1 = float(sys.argv[1])
        num2 = float(sys.argv[2])
        operation = sys.argv[3].lower()
        
        operation_map = {
            'add': 'addition',
            'addition': 'addition',
            'subtract': 'subtract',
            'multiply': 'multiply',
            'divide': 'divide'
        }
        
        op = operation_map.get(operation)
        if not op:
            print(f"Unknown operation: {operation}")
            print("Supported operations: add, subtract, multiply, divide")
            sys.exit(1)
        
        # Try to perform the calculation
        try:
            if op == 'divide' and num2 == 0:
                print("Cannot divide by zero.")
                sys.exit(1)
                
            result = Calculator.compute(op, num1, num2)
            print(f"The result of {num1} {operation} {num2} is equal to {result}")
        except ZeroDivisionError:
            print("Cannot divide by zero.")
        except Exception as e:
            print(f"An error occurred: {e}")
    except ValueError:
        print("Invalid numeric input. Both num1 and num2 must be numbers.")
        sys.exit(1)

def display_help():
    """Display help information."""
    print("\n" + "╔" + "═" * 58 + "╗")
    print(f"║{'CALCULATOR HELP':^58}║")
    print("╠" + "═" * 58 + "╣")
    print("║  This calculator provides the following functionality:        ║")
    print("║                                                               ║")
    print("║  • Basic arithmetic: add, subtract, multiply, divide          ║")
    print("║  • Advanced operations: power, sqrt, factorial                ║")
    print("║  • Calculation history with undo/redo                         ║")
    print("║                                                               ║")
    print("║  To use the calculator:                                       ║")
    print("║  1. Enter the number corresponding to the desired command     ║")
    print("║  2. Follow the prompts to input numbers                       ║")
    print("║  3. View the result                                           ║")
    print("║                                                               ║")
    print("║  Examples:                                                    ║")
    print("║    - Enter '1' to add two numbers                             ║")
    print("║    - Enter 'menu' to see available commands                   ║")
    print("║    - Enter 'quit' to exit                                     ║")
    print("╚" + "═" * 58 + "╝")

def start_repl():
    """Start the Read-Eval-Print Loop interface."""
    display_welcome()
    
    # Discover and load plugins
    discover_plugins()
    
    # Print available commands
    commands = get_available_commands()
    if commands:
        logger.info(f"Available commands: {', '.join(commands)}")
    
    display_menu(commands)
    
    while True:
        try:
            user_input = input("Enter command (or 'menu', 'help', 'exit'): ").strip().lower()
            if user_input in ['quit', 'exit', 'q']:
                print("\n" + "╔" + "═" * 58 + "╗")
                print(f"║{'GOODBYE!':^58}║")
                print(f"║{'Thank you for using the Advanced Calculator':^58}║")
                print("╚" + "═" * 58 + "╝")
                break
            if user_input == 'menu':
                display_menu(commands)
                continue
            if user_input == 'help':
                display_help()
                continue
            if user_input == 'clear':
                print("Calculator reset.")
                continue
            cmd_name = user_input
            if cmd_name in commands:
                # Determine argument prompt based on command
                if cmd_name in ['add', 'subtract', 'multiply', 'divide', 'power', 'logbase']:
                    nums_str = input("Enter two numbers (comma or space separated): ")
                    nums = [float(x) for x in nums_str.replace(',', ' ').split() if x.strip()]
                    if len(nums) != 2:
                        print("Error: Two numbers required.")
                        continue
                    try:
                        result = execute_and_log(cmd_name, nums, Calculator, history_manager)
                        print(f"RESULT: {result}")
                    except Exception as e:
                        logger.error(f"Error executing command {cmd_name}: {e}")
                        print(f"ERROR: {e}")
                elif cmd_name in ['sqrt', 'exp', 'log', 'abs']:
                    num_str = input("Enter a number: ")
                    try:
                        num = float(num_str)
                    except Exception:
                        print("Invalid input.")
                        continue
                    try:
                        result = execute_and_log(cmd_name, [num], Calculator, history_manager)
                        print(f"RESULT: {result}")
                    except Exception as e:
                        logger.error(f"Error executing command {cmd_name}: {e}")
                        print(f"ERROR: {e}")
                elif cmd_name in ['max', 'min', 'mean', 'median', 'mode', 'stdev']:
                    nums_str = input("Enter numbers (comma or space separated): ")
                    nums = [float(x) for x in nums_str.replace(',', ' ').split() if x.strip()]
                    if not nums:
                        print(f"Error: At least one number required.")
                        continue
                    try:
                        result = execute_and_log(cmd_name, nums, Calculator, history_manager)
                        print(f"RESULT: {result}")
                    except Exception as e:
                        logger.error(f"Error executing command {cmd_name}: {e}")
                        print(f"ERROR: {e}")
                else:
                    # Other commands (use original logic, but remove history_manager.add_entry calls)
                    try:
                        result = execute_command(cmd_name)
                        print(f"RESULT: {result}")
                    except Exception as e:
                        logger.error(f"Error executing command {cmd_name}: {e}")
                        print(f"ERROR: {e}")
            else:
                print(f"Unknown command: {user_input}")
                print("Type 'menu' to see available commands or 'help' for assistance.")
        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting.")
            break
        except Exception as e:
            logger.error(f"Unexpected error in REPL: {e}")
            print(f"An unexpected error occurred: {e}")

# --- Helper for command execution and history logging ---
def execute_and_log(cmd_name, args, calculator, history_manager):
    result = execute_command(cmd_name, *args)
    try:
        from src.calculator import Calculation
        # Arithmetic and binary
        if cmd_name in ['add', 'subtract', 'multiply', 'divide', 'power', 'logbase']:
            calc = Calculation(cmd_name, float(args[0]), float(args[1]), result)
        # Single-argument ops
        elif cmd_name in ['sqrt', 'exp', 'log', 'abs']:
            calc = Calculation(cmd_name, float(args[0]), None, result)
        # Stats (store first two numbers, or None)
        elif cmd_name in ['max', 'min', 'mean', 'median', 'mode', 'stdev']:
            calc = Calculation(cmd_name, float(args[0]), float(args[1]) if len(args) > 1 else None, result)
        else:
            calc = Calculation(cmd_name, None, None, result)
        history_manager.save_calculation(calc)
    except Exception as e:
        logger.error(f"Failed to save history: {e}")
    return result

def main():
    """Main entry point for the calculator application."""
    # Log application start
    logger.info("Calculator application starting")
    
    # Handle command line arguments if provided
    if len(sys.argv) > 1:
        logger.info("Running in CLI mode")
        handle_cli_args()
    else:
        # Otherwise start REPL
        logger.info("Starting REPL mode")
        start_repl()
    
    # Log application end
    logger.info("Calculator application exiting")

if __name__ == "__main__":
    main()
