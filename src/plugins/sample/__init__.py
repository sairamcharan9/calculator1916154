"""
Sample plugin module for demonstration purposes.
Shows how to create and register custom commands.
"""

import logging
from src.commands.command_base import Command
from src.calculator import Calculator, Calculation

# Get logger
logger = logging.getLogger('calculator.plugins.sample')

class MenuCommand(Command):
    """Command to display menu of available commands."""
    
    @property
    def name(self) -> str:
        return "menu"
    
    def execute(self) -> str:
        """
        Display menu of available commands.
        
        Returns:
            str: Menu text listing available commands
        """
        from main import display_menu
        display_menu()
        return "Menu displayed"

# Plugin registry for dynamic discovery
PLUGIN_REGISTRY = {}

def register_commands(command_registry):
    """
    Register sample commands to the global command registry.
    
    Args:
        command_registry (dict): The global command registry
    """
    # Create command instances
    commands = [
        MenuCommand()
    ]
    
    # Register each command
    for cmd in commands:
        command_registry[cmd.name] = cmd
        logger.info(f"Registered sample command: {cmd.name}")
    
    return command_registry
