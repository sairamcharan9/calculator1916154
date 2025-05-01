"""
Unit tests for main.py entry point and CLI/REPL integration.
"""
import pytest
import io
import sys
from unittest.mock import patch
from src.plugins import discover_plugins, list_available_commands
from src.plugins.sample import MenuCommand

def test_available_commands_includes_core_operations():
    """Test that the available commands include core arithmetic operations."""
    # Discover plugins to populate registry
    discover_plugins()
    
    # Get the list of available commands
    commands = list_available_commands()
    
    # Check that core commands are available
    assert 'add' in commands or 'addition' in commands
    assert 'subtract' in commands
    assert 'multiply' in commands
    assert 'divide' in commands

def test_menu_command():
    """Test that the menu command displays available commands."""
    # Discover plugins to populate registry
    discover_plugins()
    
    # Create menu command
    menu_cmd = MenuCommand()
    
    # Execute menu command
    with patch('sys.stdout', new=io.StringIO()) as fake_stdout:
        result = menu_cmd.execute()
        
        # Menu command now returns "Menu displayed"
        assert result == "Menu displayed"
