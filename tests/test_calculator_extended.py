"""
Extended test coverage for the Calculator class.
Focuses on methods that are not adequately covered by existing tests.
"""

import pytest
import os
import tempfile
import pandas as pd
from src.calculator import Calculator, Calculation
from unittest.mock import patch, MagicMock
import math


class TestCalculatorExtended:
    """Extended tests for Calculator class to improve coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Clear history before each test
        Calculator.clear_history()
        Calculator.undo_stack.clear()
    
    def teardown_method(self):
        """Tear down test fixtures."""
        # Clean up after each test
        Calculator.clear_history()
        Calculator.undo_stack.clear()
    
    def test_format_history(self):
        """Test format_history method."""
        # Test empty history
        assert "No calculations recorded" in Calculator.format_history()
        
        # Add some calculations and test format
        Calculator.add_to_history(Calculation("add", 2, 3, 5))
        Calculator.add_to_history(Calculation("subtract", 10, 4, 6))
        
        formatted = Calculator.format_history()
        assert "2 add 3 = 5" in formatted
        assert "10 subtract 4 = 6" in formatted
    
    def test_undo_redo_edge_cases(self):
        """Test undo and redo with empty history and stack."""
        # Test undo with empty history
        assert Calculator.undo() is None
        
        # Add calculation, undo it, then test redo
        calc = Calculation("add", 5, 5, 10)
        Calculator.add_to_history(calc)
        
        # Verify undo works
        undone = Calculator.undo()
        assert undone == calc
        assert len(Calculator.history) == 0
        assert len(Calculator.undo_stack) == 1
        
        # Verify redo works
        redone = Calculator.redo()
        assert redone == calc
        assert len(Calculator.history) == 1
        assert len(Calculator.undo_stack) == 0
        
        # Test redo with empty undo stack
        assert Calculator.redo() is None
    
    def test_save_history(self):
        """Test save_history method."""
        # Create temp file for testing
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
            temp_path = temp.name
        
        try:
            # Add some calculations
            Calculator.add_to_history(Calculation("add", 2, 3, 5))
            Calculator.add_to_history(Calculation("multiply", 4, 5, 20))
            
            # Save history to file
            Calculator.save_history(temp_path)
            
            # Verify file exists and has content
            assert os.path.exists(temp_path)
            assert os.path.getsize(temp_path) > 0
            
            # Read the file and verify content
            df = pd.read_csv(temp_path)
            assert len(df) == 2
            assert 'operation' in df.columns
            assert 'add' in df['operation'].values
            assert 'multiply' in df['operation'].values
            
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_load_history(self):
        """Test load_history method."""
        # Create temp file with test data
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as temp:
            temp_path = temp.name
            
            # Create test data
            data = [
                {'operation': 'add', 'num1': 5, 'num2': 7, 'result': 12},
                {'operation': 'divide', 'num1': 10, 'num2': 2, 'result': 5}
            ]
            pd.DataFrame(data).to_csv(temp_path, index=False)
        
        try:
            # Clear history and load from file
            Calculator.clear_history()
            Calculator.load_history(temp_path)
            
            # Verify history was loaded
            history = Calculator.get_history()
            assert len(history) == 2
            
            # Verify calculations were loaded correctly
            assert history[0].operation == 'add'
            assert history[0].num1 == 5
            assert history[0].num2 == 7
            assert history[0].result == 12
            
            assert history[1].operation == 'divide'
            assert history[1].num1 == 10
            assert history[1].num2 == 2
            assert history[1].result == 5
            
        finally:
            # Clean up
            if os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def test_compute_scientific_operations(self):
        """Test compute method with scientific operations."""
        # Test sqrt
        result = Calculator.compute('sqrt', 16)
        assert result == 4
        
        # Test log
        result = Calculator.compute('log', math.e)
        assert math.isclose(result, 1.0)
        
        # Test sin
        result = Calculator.compute('sin', 0)
        assert math.isclose(result, 0.0)
        
        # Test cos
        result = Calculator.compute('cos', 0)
        assert math.isclose(result, 1.0)
        
        # Test tan
        result = Calculator.compute('tan', 0)
        assert math.isclose(result, 0.0)
        
        # Test invalid operation
        with pytest.raises(ValueError):
            Calculator.compute('invalid_op', 1)


# Add tests for the get_inputs method which is part of the REPL UI
class TestCalculatorUI:
    """Tests for Calculator UI methods."""
    
    @patch('builtins.input')
    def test_get_inputs_valid(self, mock_input):
        """Test get_inputs with valid numeric inputs."""
        mock_input.side_effect = ["10", "5"]
        num1, num2 = Calculator.get_inputs()
        assert num1 == 10
        assert num2 == 5
    
    @patch('builtins.input')
    def test_get_inputs_quit(self, mock_input):
        """Test get_inputs with quit command."""
        # Test quitting on first prompt
        mock_input.side_effect = ["quit", "5"]
        num1, num2 = Calculator.get_inputs()
        assert num1 is None
        assert num2 is None
        
        # Test quitting on second prompt
        mock_input.reset_mock()
        mock_input.side_effect = ["10", "quit"]
        num1, num2 = Calculator.get_inputs()
        assert num1 is None
        assert num2 is None
    
    @patch('builtins.input')
    def test_get_inputs_invalid(self, mock_input):
        """Test get_inputs with invalid inputs."""
        mock_input.side_effect = ["abc", "5"]
        num1, num2 = Calculator.get_inputs()
        assert num1 is None
        assert num2 is None
