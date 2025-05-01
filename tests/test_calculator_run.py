"""
Tests for the Calculator run method and REPL functionality.
"""

import pytest
from unittest.mock import patch, MagicMock
import os
import tempfile
from src.calculator import Calculator, Calculation


class TestCalculatorRun:
    """Tests for the Calculator's run method and REPL functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        Calculator.clear_history()
        Calculator.undo_stack.clear()
    
    def teardown_method(self):
        """Tear down test fixtures."""
        Calculator.clear_history()
        Calculator.undo_stack.clear()
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_exit(self, mock_print, mock_input):
        """Test exiting the calculator."""
        # Set up inputs to immediately exit
        mock_input.side_effect = ["14"]
        
        # Run the calculator
        Calculator.run()
        
        # Check that the exit message was printed
        exit_found = False
        for call_args in mock_print.call_args_list:
            args, _ = call_args
            if len(args) > 0 and "Exiting calculator. Goodbye!" in args[0]:
                exit_found = True
                break
        assert exit_found, "Exit message not found"
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_add(self, mock_print, mock_input):
        """Test performing an addition in the REPL."""
        # Set up inputs for performing addition and then exiting
        mock_input.side_effect = ["1", "5", "7", "14"]
        
        # Run the calculator
        Calculator.run()
        
        # Check that the addition result was printed and added to history
        result_found = False
        for call_args in mock_print.call_args_list:
            args, _ = call_args
            if len(args) > 0 and "The result is: 12" in args[0]:
                result_found = True
                break
        assert result_found, "Result print message not found"
        
        history = Calculator.get_history()
        assert len(history) == 1
        assert history[0].operation == "add"
        assert history[0].num1 == 5
        assert history[0].num2 == 7
        assert history[0].result == 12
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_subtract(self, mock_print, mock_input):
        """Test performing a subtraction in the REPL."""
        mock_input.side_effect = ["2", "10", "4", "14"]
        
        Calculator.run()
        
        result_found = False
        for call_args in mock_print.call_args_list:
            args, _ = call_args
            if len(args) > 0 and "The result is: 6" in args[0]:
                result_found = True
                break
        assert result_found, "Result print message not found"
        
        history = Calculator.get_history()
        assert len(history) == 1
        assert history[0].operation == "subtract"
        assert history[0].num1 == 10
        assert history[0].num2 == 4
        assert history[0].result == 6
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_multiply(self, mock_print, mock_input):
        """Test performing multiplication in the REPL."""
        mock_input.side_effect = ["3", "6", "7", "14"]
        
        Calculator.run()
        
        result_found = False
        for call_args in mock_print.call_args_list:
            args, _ = call_args
            if len(args) > 0 and "The result is: 42" in args[0]:
                result_found = True
                break
        assert result_found, "Result print message not found"
        
        history = Calculator.get_history()
        assert len(history) == 1
        assert history[0].operation == "multiply"
        assert history[0].num1 == 6
        assert history[0].num2 == 7
        assert history[0].result == 42
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_divide(self, mock_print, mock_input):
        """Test performing division in the REPL."""
        mock_input.side_effect = ["4", "10", "2", "14"]
        
        Calculator.run()
        
        result_found = False
        for call_args in mock_print.call_args_list:
            args, _ = call_args
            if len(args) > 0 and "The result is: 5.0" in args[0]:
                result_found = True
                break
        assert result_found, "Result print message not found"
        
        history = Calculator.get_history()
        assert len(history) == 1
        assert history[0].operation == "divide"
        assert history[0].num1 == 10
        assert history[0].num2 == 2
        assert history[0].result == 5.0
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_divide_by_zero(self, mock_print, mock_input):
        """Test handling division by zero."""
        mock_input.side_effect = ["4", "10", "0", "14"]
        
        Calculator.run()
        
        error_found = False
        for call_args in mock_print.call_args_list:
            args, _ = call_args
            if len(args) > 0 and "Cannot divide by zero." in args[0]:
                error_found = True
                break
        assert error_found, "Division by zero error message not found"
        
        # History should remain empty
        history = Calculator.get_history()
        assert len(history) == 0
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_history(self, mock_print, mock_input):
        """Test viewing history in the REPL."""
        # First add a calculation to history
        Calculator.add_to_history(Calculation("add", 2, 3, 5))
        
        # Set up inputs to view history and then exit
        mock_input.side_effect = ["5", "14"]
        
        Calculator.run()
        
        # Check that history was displayed
        history_output_found = False
        for call_args in mock_print.call_args_list:
            args, _ = call_args
            if len(args) > 0 and "2 add 3 = 5" in args[0]:
                history_output_found = True
                break
        
        assert history_output_found
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_clear_history(self, mock_print, mock_input):
        """Test clearing history in the REPL."""
        # First add a calculation to history
        Calculator.add_to_history(Calculation("add", 2, 3, 5))
        
        # Set up inputs to clear history and then exit
        mock_input.side_effect = ["6", "14"]
        
        Calculator.run()
        
        # Check that history was cleared
        assert len(Calculator.get_history()) == 0
        
        message_found = False
        for call_args in mock_print.call_args_list:
            args, _ = call_args
            if len(args) > 0 and "History has been cleared." in args[0]:
                message_found = True
                break
        assert message_found, "History cleared message not found"
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_undo(self, mock_print, mock_input):
        """Test undoing a calculation in the REPL."""
        # First add a calculation to history
        Calculator.add_to_history(Calculation("add", 2, 3, 5))
        
        # Set up inputs to undo and then exit
        mock_input.side_effect = ["7", "14"]
        
        Calculator.run()
        
        # Check that the calculation was undone
        assert len(Calculator.get_history()) == 0
        assert len(Calculator.undo_stack) == 1
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_redo(self, mock_print, mock_input):
        """Test redoing a calculation in the REPL."""
        # First add a calculation and then undo it
        calc = Calculation("add", 2, 3, 5)
        Calculator.add_to_history(calc)
        Calculator.undo()
        
        # Set up inputs to redo and then exit
        mock_input.side_effect = ["8", "14"]
        
        Calculator.run()
        
        # Check that the calculation was redone
        history = Calculator.get_history()
        assert len(history) == 1
        assert history[0] == calc
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_sqrt(self, mock_print, mock_input):
        """Test performing square root in the REPL."""
        mock_input.side_effect = ["9", "16", "14"]
        
        Calculator.run()
        
        result_found = False
        for call_args in mock_print.call_args_list:
            args, _ = call_args
            if len(args) > 0 and "The result is: 4.0" in args[0]:
                result_found = True
                break
        assert result_found, "Result print message not found"
        
        history = Calculator.get_history()
        assert len(history) == 1
        assert history[0].operation == "sqrt"
        assert history[0].num1 == 16
        assert history[0].result == 4.0
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_log(self, mock_print, mock_input):
        """Test performing natural logarithm in the REPL."""
        # Using e as input should yield 1.0
        import math
        mock_input.side_effect = ["10", str(math.e), "14"]
        
        Calculator.run()
        
        # Find the result in the print calls
        result_found = False
        for call_args in mock_print.call_args_list:
            args, _ = call_args
            if len(args) > 0 and "The result is:" in args[0]:
                # Check that the result is approximately 1.0 (allowing for floating point precision)
                result_str = args[0].split(":")[1].strip()
                try:
                    result = float(result_str)
                    if abs(result - 1.0) < 0.0001:  # Close enough to 1.0
                        result_found = True
                        break
                except ValueError:
                    pass
        
        assert result_found
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_trigonometric(self, mock_print, mock_input):
        """Test performing trigonometric operations in the REPL."""
        # Test sin(0) which should be 0
        mock_input.side_effect = ["11", "0", "14"]
        
        Calculator.run()
        
        result_found = False
        for call_args in mock_print.call_args_list:
            args, _ = call_args
            if len(args) > 0 and "The result is: 0.0" in args[0]:
                result_found = True
                break
        assert result_found, "Result print message not found"
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_invalid_choice(self, mock_print, mock_input):
        """Test handling invalid menu choices."""
        mock_input.side_effect = ["invalid", "14"]
        
        Calculator.run()
        
        error_found = False
        for call_args in mock_print.call_args_list:
            args, _ = call_args
            if len(args) > 0 and "Invalid choice" in args[0]:
                error_found = True
                break
        assert error_found, "Invalid choice message not found"
    
    @patch('builtins.input')
    @patch('builtins.print')
    def test_run_invalid_numbers(self, mock_print, mock_input):
        """Test handling invalid numeric inputs."""
        mock_input.side_effect = ["1", "not_a_number", "3", "14"]
        
        Calculator.run()
        
        error_found = False
        for call_args in mock_print.call_args_list:
            args, _ = call_args
            if len(args) > 0 and "Invalid number" in args[0]:
                error_found = True
                break
        assert error_found, "Invalid number message not found"
    
    @patch('builtins.input')
    def test_get_inputs_valid(self, mock_input):
        """Test get_inputs with valid inputs."""
        mock_input.side_effect = ["5", "7"]
        
        num1, num2 = Calculator.get_inputs()
        
        assert num1 == 5
        assert num2 == 7
    
    @patch('builtins.input')
    def test_get_inputs_quit_first(self, mock_input):
        """Test get_inputs with quit on first input."""
        mock_input.side_effect = ["quit", "7"]
        
        num1, num2 = Calculator.get_inputs()
        
        assert num1 is None
        assert num2 is None
    
    @patch('builtins.input')
    def test_get_inputs_quit_second(self, mock_input):
        """Test get_inputs with quit on second input."""
        mock_input.side_effect = ["5", "quit"]
        
        num1, num2 = Calculator.get_inputs()
        
        assert num1 is None
        assert num2 is None
    
    @patch('builtins.input')
    def test_get_inputs_invalid(self, mock_input):
        """Test get_inputs with invalid inputs."""
        mock_input.side_effect = ["abc", "7"]
        
        num1, num2 = Calculator.get_inputs()
        
        assert num1 is None
        assert num2 is None
