"""
Arithmetic operations plugin module.
Provides basic arithmetic operations for the calculator.
"""

import logging
from src.commands.command_base import Command
from src.commands.arithmetic_commands import (
    AddCommand, SubtractCommand, MultiplyCommand, DivideCommand
)

# Get logger
logger = logging.getLogger('calculator.plugins.arithmetic')

# Plugin registry for dynamic discovery
PLUGIN_REGISTRY = {}

def register_commands(command_registry):
    """
    Register arithmetic commands to the global command registry.
    
    Args:
        command_registry (dict): The global command registry
    """
    # Create command instances
    commands = [
        AddCommand(),
        SubtractCommand(),
        MultiplyCommand(),
        DivideCommand()
    ]
    
    # Register each command
    for cmd in commands:
        command_registry[cmd.name] = cmd
        logger.info(f"Registered arithmetic command: {cmd.name}")
    
    return command_registry
