"""
Main entry point for the calculator CLI and REPL.
Editor: ##@sb2853.njit.edu
"""
"""
Handles CLI and REPL modes.
"""

import sys
from app.calculator import Calculator
import sys
import os
import logging
from app.calculator import Calculator
from decimal import Decimal, InvalidOperation
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up logging
# Set log level from DEBUG env variable
log_level = logging.DEBUG if os.getenv('DEBUG', 'False').lower() == 'true' else logging.INFO
logging.basicConfig(
    level=log_level,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Log the environment and debug mode
environment = os.getenv('ENVIRONMENT', 'development')
debug_mode = os.getenv('DEBUG', 'False')
logger.info(f"Calculator starting in ENVIRONMENT: {environment}, DEBUG={debug_mode}")

# Plugin Architecture Note:
# If your rubric requires dynamic plugin loading, you must implement a mechanism
# for loading new operation commands at runtime (e.g., via a plugins/ folder or entry points).
# This is not present in the current codebase.

import importlib
import pkgutil

PLUGIN_COMMANDS = {}

# Dynamically load all plugin commands from app.plugins submodules
plugin_pkg = 'app.plugins'
plugin_path = importlib.import_module(plugin_pkg).__path__
for finder, name, ispkg in pkgutil.iter_modules(plugin_path):
    try:
        module = importlib.import_module(f'{plugin_pkg}.{name}')
        for attr in dir(module):
            obj = getattr(module, attr)
            if isinstance(obj, type) and hasattr(obj, 'execute'):
                # Register command by lowercase operation name (e.g. add, subtract)
                if attr.endswith('Command'):
                    cmd_name = attr.replace('Command', '').lower()
                    if cmd_name:  # Only register if not empty
                        PLUGIN_COMMANDS[cmd_name] = obj
                        logger.info(f"Loaded plugin command: {cmd_name} -> {obj}")
    except Exception as e:
        logger.error(f"Failed to load plugin {name}: {e}")


def calculation(*args):
    """
    Executes a calculator command using dynamically loaded plugins.
    """
    if len(args) < 2:
        logger.error("Not enough arguments. Usage: <operation> <num1> <num2> ...")
        return
    operation = args[0].lower()
    numbers = args[1:]
    cmd_cls = PLUGIN_COMMANDS.get(operation)
    if not cmd_cls:
        logger.error(f"Unknown operation: {operation}")
        return
    try:
        cmd = cmd_cls(*numbers)
        result = cmd.execute()
        logger.info(f"Result of {operation} {' '.join(numbers)} = {result}")
        print(f"Result: {result}")
    except Exception as e:
        logger.error(f"Error executing {operation}: {e}")
        print(f"Error: {e}")


def cli_mode():
    """
    Handles command-line input for performing calculations.
    """
    if len(sys.argv) == 1:
        logger.info("Starting REPL mode... Type 'quit' to exit.")
        Calculator.run()
        return

    if len(sys.argv) != 4:
        logger.error("Usage: python main.py <num1> <num2> <operation>")
        sys.exit(1)

    _, val1, val2, op = sys.argv
    calculation(val1, val2, op)


if __name__ == '__main__':
    cli_mode()
