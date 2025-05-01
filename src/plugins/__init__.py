"""
Plugin loader module.
Implements dynamic plugin discovery and loading.
"""

import importlib.util
import inspect
import logging
import os
import sys
from typing import Dict, Any, List, Type, Callable, Optional
from unittest.mock import MagicMock  # Import MagicMock

from src.commands.command_base import Command

# Get the logger
logger = logging.getLogger('calculator.plugins')

# Registry of loaded plugins
PLUGIN_REGISTRY: Dict[str, Any] = {}

# Registry of loaded commands
COMMAND_REGISTRY: Dict[str, Command] = {}

def register_command(command: Command) -> None:
    """
    Register a command in the COMMAND_REGISTRY.
    
    Args:
        command (Command): The command to register
    """
    COMMAND_REGISTRY[command.name] = command
    logger.debug(f"Registered command: {command.name}")

def discover_plugins(plugin_dir: Optional[str] = None) -> Dict[str, Command]:
    """
    Discover and load plugins from the specified directory.
    
    Args:
        plugin_dir (str, optional): Directory to search for plugins
        
    Returns:
        Dict[str, Command]: Dictionary of registered commands
    """
    # If no plugin directory is specified, use the default
    if plugin_dir is None:
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
    
    logger.info(f"Discovering plugins in: {plugin_dir}")
    
    # Load plugins from submodules
    _discover_plugins_in_directory(plugin_dir)
    
    return COMMAND_REGISTRY

def _discover_plugins_in_directory(directory: str) -> None:
    """
    Discover plugins in a directory and register their commands.
    """
    for entry in os.listdir(directory):
        entry_path = os.path.join(directory, entry)
        if entry.startswith("__"):  # skip __pycache__ etc
            continue
        if os.path.isdir(entry_path):
            # Try to import the submodule
            module_name = f"src.plugins.{entry}"
            try:
                module = importlib.import_module(module_name)
                # If the module has a register_commands function, call it
                if hasattr(module, "register_commands"):
                    module.register_commands(COMMAND_REGISTRY)
                    logger.info(f"Registered commands from plugin: {module_name}")
                else:
                    logger.warning(f"Plugin {module_name} does not have register_commands.")
            except Exception as e:
                logger.error(f"Error importing plugin {module_name}: {e}")
        elif entry.endswith(".py") and entry != "__init__.py":
            # Try to import the module
            module_name = f"src.plugins.{os.path.splitext(entry)[0]}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, "register_commands"):
                    module.register_commands(COMMAND_REGISTRY)
                    logger.info(f"Registered commands from plugin: {module_name}")
                else:
                    logger.warning(f"Plugin {module_name} does not have register_commands.")
            except Exception as e:
                logger.error(f"Error importing plugin {module_name}: {e}")

    # Ensure all built-in plugins are registered
    from src.plugins import arithmetic, data, scientific, sample
    for plugin_mod in [arithmetic, data, scientific, sample]:
        if hasattr(plugin_mod, "register_commands"):
            plugin_mod.register_commands(COMMAND_REGISTRY)

def get_plugin_function(name: str) -> Optional[Callable]:
    """
    Get a plugin function by name.
    
    Args:
        name (str): Name of the plugin function
        
    Returns:
        Callable or None: The plugin function or None if not found
    """
    return PLUGIN_REGISTRY.get(name)

def list_available_commands() -> List[str]:
    """
    List all available commands.
    
    Returns:
        List[str]: List of command names
    """
    return list(COMMAND_REGISTRY.keys())

def get_command(name: str) -> Optional[Command]:
    """
    Get a command by name.
    
    Args:
        name (str): Name of the command
        
    Returns:
        Command or None: The command or None if not found
    """
    return COMMAND_REGISTRY.get(name)

def get_available_commands():
    """Return a list of available command names from all plugin modules."""
    return list(COMMAND_REGISTRY.keys())

def execute_command(name, *args, **kwargs):
    """Execute a command by name from the COMMAND_REGISTRY."""
    cmd = COMMAND_REGISTRY.get(name)
    if cmd is None:
        return None
    return cmd.execute(*args, **kwargs)
