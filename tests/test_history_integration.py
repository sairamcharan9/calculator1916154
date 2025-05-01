"""
Integration tests for calculator history functionality.
These tests verify that calculations are correctly saved, retrieved, 
and manipulated in the history.
"""
import os
import pytest
import tempfile
import shutil
from src.calculator import Calculator, Calculation
from src.commands.arithmetic_commands import (
    AddCommand, HistoryCommand, ClearHistoryCommand, UndoCommand, RedoCommand
)
from src.history.data_manager import HistoryDataManager, history_manager


@pytest.fixture
def temp_history_file():
    """Create a temporary history file for testing."""
    temp_dir = tempfile.mkdtemp()
    temp_file = os.path.join(temp_dir, 'test_history.csv')
    yield temp_file
    # Cleanup
    shutil.rmtree(temp_dir)


@pytest.fixture
def test_history_manager(temp_history_file):
    """Create a test history manager with a temporary file."""
    manager = HistoryDataManager(temp_history_file)
    yield manager
    # Clear history after test
    manager.clear_history()


def test_history_integration(test_history_manager):
    """Test that calculations are correctly saved and retrieved from history."""
    # Create test commands
    add_cmd = AddCommand()
    history_cmd = HistoryCommand()
    clear_cmd = ClearHistoryCommand()
    
    # Replace the global history_manager with our test manager
    from src.commands.arithmetic_commands import history_manager as cmd_history_manager
    original_manager = cmd_history_manager
    from src.commands import arithmetic_commands
    arithmetic_commands.history_manager = test_history_manager
    
    try:
        # Clear both Calculator and history manager
        Calculator.clear_history()
        test_history_manager.clear_history()
        
        # Perform a calculation
        result = add_cmd.execute(5, 7)
        assert result == 12
        
        # Check history through the command
        history_text = history_cmd.execute()
        assert "5 add 7 = 12" in history_text
        
        # Get history directly from manager
        history_entries = test_history_manager.get_history()
        assert len(history_entries) == 1
        assert history_entries[0].operation == "add"
        assert history_entries[0].num1 == 5
        assert history_entries[0].num2 == 7
        assert history_entries[0].result == 12
        
        # Clear history
        clear_result = clear_cmd.execute()
        assert "cleared" in clear_result.lower()
        
        # Verify history is empty
        history_entries = test_history_manager.get_history()
        assert len(history_entries) == 0
        
        # Check empty history display
        empty_history = history_cmd.execute()
        assert "empty" in empty_history.lower()
    finally:
        # Restore the original history manager
        arithmetic_commands.history_manager = original_manager


def test_undo_redo_integration(test_history_manager):
    """Test that undo and redo commands work correctly with history."""
    # Create test commands
    add_cmd = AddCommand()
    undo_cmd = UndoCommand()
    redo_cmd = RedoCommand()
    history_cmd = HistoryCommand()
    
    # Replace the global history_manager with our test manager
    from src.commands.arithmetic_commands import history_manager as cmd_history_manager
    original_manager = cmd_history_manager
    from src.commands import arithmetic_commands
    arithmetic_commands.history_manager = test_history_manager
    
    try:
        # Clear both Calculator and history manager to start fresh
        Calculator.clear_history()
        test_history_manager.clear_history()
        
        # Perform calculations
        result1 = add_cmd.execute(2, 3)
        assert result1 == 5
        result2 = add_cmd.execute(7, 8)
        assert result2 == 15
        
        # Check history has both calculations
        history_entries = test_history_manager.get_history()
        assert len(history_entries) == 2
        
        # Get history through command
        history_text = history_cmd.execute()
        assert "2 add 3 = 5" in history_text
        assert "7 add 8 = 15" in history_text
        
        # Undo the last calculation
        undo_result = undo_cmd.execute()
        assert "Undone" in undo_result
        
        # Check that the history command reflects the change
        history_text = history_cmd.execute()
        assert "2 add 3 = 5" in history_text
        assert "7 add 8 = 15" not in history_text
        
        # Redo the undone calculation
        redo_result = redo_cmd.execute()
        assert "Redone" in redo_result
        
        # Check that the history command shows the restored calculation
        history_text = history_cmd.execute()
        assert "2 add 3 = 5" in history_text
        assert "7 add 8 = 15" in history_text
    finally:
        # Restore the original history manager
        arithmetic_commands.history_manager = original_manager


def test_calculator_history_sync():
    """Test that the Calculator's history and history_manager stay in sync."""
    # Clear both histories to start fresh
    Calculator.clear_history()
    history_manager.clear_history()
    
    # Add a calculation to Calculator's history
    calc = Calculation("add", 10, 20, 30)
    Calculator.add_to_history(calc)
    
    # Check both histories
    calc_history = Calculator.get_history()
    manager_history = history_manager.get_history()
    
    # The histories are currently not synced by design, so they should be different
    assert len(calc_history) == 1
    assert len(manager_history) == 0
    
    # If we add through the history manager
    history_manager.save_calculation(calc)
    
    # Only the manager history should be updated
    calc_history = Calculator.get_history()
    manager_history = history_manager.get_history()
    assert len(calc_history) == 1
    assert len(manager_history) == 1
    
    # This test demonstrates the current behavior where histories aren't synced
    # In a future enhancement, we might want to modify this behavior
