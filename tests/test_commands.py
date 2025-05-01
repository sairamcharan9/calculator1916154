"""
Unit tests for the commands module.
"""
import pytest
from unittest.mock import patch, MagicMock
import math
import numpy as np
from src.commands.command_base import Command
from src.commands.arithmetic_commands import (
    AddCommand, SubtractCommand, MultiplyCommand, DivideCommand,
    HistoryCommand, ClearHistoryCommand, UndoCommand, RedoCommand
)
# Import scientific commands from the scientific plugin
from src.plugins.scientific import (
    AbsoluteCommand, SquareRootCommand, ExponentialCommand, LogCommand, LogBaseCommand
)
# Import statistical commands from the appropriate plugin
from src.plugins.data import (
    MaxCommand, MinCommand, MeanCommand, MedianCommand, ModeCommand, StandardDeviationCommand
)
from src.commands.power_command import PowerCommand
from src.calculator import Calculator, Calculation

class TestCommandBase:
    """Tests for the Command base class."""
    
    def test_command_base_is_abstract(self):
        """Test that Command is effectively abstract."""
        # Attempting to instantiate Command directly should fail
        with pytest.raises(TypeError):
            Command()
        
        # But subclassing and implementing required methods should work
        class ConcreteCommand(Command):
            @property
            def name(self):
                return "concrete"
            
            def execute(self, *args, **kwargs):
                return "executed"
        
        cmd = ConcreteCommand()
        assert cmd.name == "concrete"
        assert cmd.execute() == "executed"

class TestArithmeticCommands:
    """Tests for arithmetic commands."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Clear calculator history before each test
        Calculator.clear_history()
    
    def test_add_command(self):
        """Test AddCommand."""
        cmd = AddCommand()
        result = cmd.execute(5, 3)
        assert result == 8
        assert cmd.name == "add"
        
        # Check that the calculation was added to history
        history = Calculator.history
        assert len(history) == 1
        assert history[0].operation == "add"  # The operation string matches the command name
        assert history[0].num1 == 5
        assert history[0].num2 == 3
        assert history[0].result == 8
    
    def test_subtract_command(self):
        """Test SubtractCommand."""
        cmd = SubtractCommand()
        result = cmd.execute(10, 4)
        assert result == 6
        assert cmd.name == "subtract"
        
        # Check that the calculation was added to history
        history = Calculator.history
        assert len(history) == 1
        assert history[0].operation == "subtract"  # The operation string matches the command name
        assert history[0].num1 == 10
        assert history[0].num2 == 4
        assert history[0].result == 6
    
    def test_multiply_command(self):
        """Test MultiplyCommand."""
        cmd = MultiplyCommand()
        result = cmd.execute(3, 4)
        assert result == 12
        assert cmd.name == "multiply"
        
        # Check that the calculation was added to history
        history = Calculator.history
        assert len(history) == 1
        assert history[0].operation == "multiply"  # The operation string matches the command name
        assert history[0].num1 == 3
        assert history[0].num2 == 4
        assert history[0].result == 12
    
    def test_divide_command(self):
        """Test DivideCommand."""
        cmd = DivideCommand()
        result = cmd.execute(10, 2)
        assert result == 5
        assert cmd.name == "divide"
        
        # Check that the calculation was added to history
        history = Calculator.history
        assert len(history) == 1
        assert history[0].operation == "divide"  # The operation string matches the command name
        assert history[0].num1 == 10
        assert history[0].num2 == 2
        assert history[0].result == 5
    
    def test_divide_by_zero(self):
        """Test DivideCommand with division by zero."""
        cmd = DivideCommand()
        with pytest.raises(ZeroDivisionError):
            cmd.execute(5, 0)
    
    def test_absolute_command(self):
        """Test AbsoluteCommand."""
        cmd = AbsoluteCommand()
        result = cmd.execute(-5)
        assert result == 5
        assert cmd.name == "abs"
        
        # Check that the calculation was added to history
        history = Calculator.history
        assert len(history) == 1
        assert history[0].operation == "abs"
        assert history[0].num1 == -5
        assert history[0].result == 5
    
    def test_square_root_command(self):
        """Test SquareRootCommand."""
        cmd = SquareRootCommand()
        result = cmd.execute(16)
        assert result == 4
        assert cmd.name == "sqrt"
        
        # Check that the calculation was added to history
        history = Calculator.history
        assert len(history) == 1
        assert history[0].operation == "sqrt"
        assert history[0].num1 == 16
        assert history[0].result == 4
    
    def test_square_root_negative(self):
        """Test SquareRootCommand with negative input."""
        cmd = SquareRootCommand()
        with pytest.raises(ValueError):
            cmd.execute(-1)
    
    def test_exponential_command(self):
        """Test ExponentialCommand."""
        cmd = ExponentialCommand()
        result = cmd.execute(2)
        # e^2 is approximately 7.389
        assert abs(result - 7.389) < 0.01
        assert cmd.name == "exp"
        
        # Check that the calculation was added to history
        history = Calculator.history
        assert len(history) == 1
        assert history[0].operation == "exp"
        assert history[0].num1 == 2
        assert abs(history[0].result - 7.389) < 0.01
    
    def test_log_command(self):
        """Test LogCommand."""
        cmd = LogCommand()
        result = cmd.execute(10)
        # ln(10) is approximately 2.303
        assert abs(result - 2.303) < 0.01
        assert cmd.name == "log"
        
        # Check that the calculation was added to history
        history = Calculator.history
        assert len(history) == 1
        assert history[0].operation == "log"
        assert history[0].num1 == 10
        assert abs(history[0].result - 2.303) < 0.01
    
    def test_log_base_command(self):
        """Test LogBaseCommand."""
        cmd = LogBaseCommand()
        result = cmd.execute(100, 10)
        assert result == 2
        assert cmd.name == "logbase"
        
        # Check that the calculation was added to history
        history = Calculator.history
        assert len(history) == 1
        assert history[0].operation == "logbase"
        assert history[0].num1 == 100
        assert history[0].num2 == 10
        assert history[0].result == 2
    
    def test_log_non_positive(self):
        """Test LogCommand with non-positive input."""
        cmd = LogCommand()
        with pytest.raises(ValueError):
            cmd.execute(0)
        
        with pytest.raises(ValueError):
            cmd.execute(-1)
    
    def test_log_base_non_positive(self):
        """Test LogBaseCommand with non-positive input."""
        cmd = LogBaseCommand()
        with pytest.raises(ValueError):
            cmd.execute(0, 2)
        
        with pytest.raises(ValueError):
            cmd.execute(-1, 2)
    
    def test_log_base_invalid_base(self):
        """Test LogBaseCommand with invalid base."""
        cmd = LogBaseCommand()
        with pytest.raises(ValueError):
            cmd.execute(8, 0)
        
        with pytest.raises(ValueError):
            cmd.execute(8, -1)
        
        with pytest.raises(ValueError):
            cmd.execute(8, 1)

class TestStatisticalCommands:
    """Tests for statistical commands."""
    
    def setup_method(self):
        """Set up test fixtures."""
        Calculator.clear_history()
    
    def test_max_command(self):
        """Test MaxCommand."""
        cmd = MaxCommand()
        result = cmd.execute(5, 7, 3, 8, 2)
        assert result == 8
        assert cmd.name == "max"
    
    def test_min_command(self):
        """Test MinCommand."""
        cmd = MinCommand()
        result = cmd.execute(5, 7, 3, 8, 2)
        assert result == 2
        assert cmd.name == "min"
    
    def test_mean_command(self):
        """Test MeanCommand."""
        cmd = MeanCommand()
        result = cmd.execute(2, 4, 6, 8, 10)
        assert result == 6
        assert cmd.name == "mean"
    
    def test_median_command(self):
        """Test MedianCommand."""
        cmd = MedianCommand()
        
        # Test with odd number of elements
        result = cmd.execute(2, 4, 6, 8, 10)
        assert result == 6
        
        # Test with even number of elements
        result = cmd.execute(2, 4, 6, 8)
        assert result == 5
        
        assert cmd.name == "median"
    
    def test_mode_command(self):
        """Test ModeCommand."""
        cmd = ModeCommand()
        result = cmd.execute(2, 4, 6, 4, 8, 10, 4)
        assert result == 4
        assert cmd.name == "mode"
    
    def test_mode_command_multiple_modes(self):
        """Test ModeCommand with multiple modes."""
        cmd = ModeCommand()
        # In this case, both 4 and 6 appear twice, but the algorithm should return the first one it finds
        result = cmd.execute(2, 4, 6, 4, 8, 10, 6)
        assert result in (4, 6)  # Either 4 or 6 is acceptable
    
    def test_standard_deviation_command(self):
        """Test StandardDeviationCommand."""
        cmd = StandardDeviationCommand()
        result = cmd.execute(2, 4, 6, 8, 10)
        # Expected standard deviation for [2, 4, 6, 8, 10] is √(10) ≈ 3.16
        assert math.isclose(result, 3.16227766017, rel_tol=1e-10)
        assert cmd.name == "stdev"
        
        # Test with insufficient data
        with pytest.raises(ValueError):
            cmd.execute(5)

class TestHistoryCommands:
    """Tests for history and memory commands."""
    
    def setup_method(self):
        """Set up test fixtures."""
        Calculator.clear_history()
        # Also clear history manager
        from src.history.data_manager import history_manager
        history_manager.clear_history()
    
    @patch('src.history.data_manager.history_manager.get_history')
    def test_history_command(self, mock_get_history):
        """Test HistoryCommand."""
        # Create calculations for testing
        calc1 = Calculation("add", 2, 3, 5)
        calc2 = Calculation("multiply", 5, 4, 20)
        
        # Mock get_history to return our test calculations
        mock_get_history.return_value = [calc1, calc2]
        
        cmd = HistoryCommand()
        result = cmd.execute()
        
        # Check the result
        expected_result = f"Calculation History:\n{calc1}\n{calc2}"
        assert result == expected_result
        assert cmd.name == "history"
    
    @patch('src.history.data_manager.history_manager.clear_history')
    def test_clear_history_command(self, mock_clear_history):
        """Test ClearHistoryCommand."""
        # Add some calculations to history
        from src.history.data_manager import history_manager
        history_manager.save_calculation(Calculation("add", 2, 3, 5))
        
        # Set up the mock
        mock_clear_history.return_value = None
        
        cmd = ClearHistoryCommand()
        result = cmd.execute()
        
        # Check that clear_history was called
        mock_clear_history.assert_called_once()
        
        # Check the output message
        assert result == "History has been cleared."
        assert cmd.name == "clear_history"
    
    @patch('src.calculator.Calculator.undo')
    def test_undo_command(self, mock_undo):
        """Test UndoCommand."""
        # Create a calculation for the mock to return
        calc = Calculation("add", 2, 3, 5)
        
        # Set up the mock
        mock_undo.return_value = calc
        
        cmd = UndoCommand()
        result = cmd.execute()
        
        # Check that undo was called
        mock_undo.assert_called_once()
        
        # Check the exact output message format
        assert result == f"Undone: {calc}"
        assert cmd.name == "undo"
    
    @patch('src.calculator.Calculator.undo')
    def test_undo_command_empty_history(self, mock_undo):
        """Test UndoCommand with empty history."""
        # Set up the mock to return None (empty history)
        mock_undo.return_value = None
        
        cmd = UndoCommand()
        result = cmd.execute()
        
        # Check that undo was called
        mock_undo.assert_called_once()
        
        # Check the exact output message
        assert result == "Nothing to undo."
    
    @patch('src.calculator.Calculator.redo')
    def test_redo_command(self, mock_redo):
        """Test RedoCommand."""
        # Create a calculation for the mock to return
        calc = Calculation("add", 2, 3, 5)
        
        # Set up the mock
        mock_redo.return_value = calc
        
        cmd = RedoCommand()
        result = cmd.execute()
        
        # Check that redo was called
        mock_redo.assert_called_once()
        
        # Check the exact output message format
        assert result == f"Redone: {calc}"
        assert cmd.name == "redo"
    
    @patch('src.calculator.Calculator.redo')
    def test_redo_command_empty_history(self, mock_redo):
        """Test RedoCommand with empty undo history."""
        # Set up the mock to return None (empty redo stack)
        mock_redo.return_value = None
        
        cmd = RedoCommand()
        result = cmd.execute()
        
        # Check that redo was called
        mock_redo.assert_called_once()
        
        # Check the exact output message
        assert result == "Nothing to redo."

class TestPowerCommand:
    """Tests for PowerCommand."""
    
    def setup_method(self):
        """Set up test fixtures."""
        Calculator.clear_history()
    
    def test_power_command(self):
        """Test PowerCommand."""
        cmd = PowerCommand()
        result = cmd.execute(2, 3)
        assert result == 8  # 2^3 = 8
        assert cmd.name == "power"
        
        # Check that the calculation was added to history
        history = Calculator.history
        assert len(history) == 1
        assert history[0].operation == "power"
        assert history[0].num1 == 2
        assert history[0].num2 == 3
        assert history[0].result == 8  # Also verify the stored result is correct
    
    def test_power_zero_exponent(self):
        """Test PowerCommand with zero exponent."""
        cmd = PowerCommand()
        result = cmd.execute(5, 0)
        assert result == 1
    
    def test_power_negative_exponent(self):
        """Test PowerCommand with negative exponent."""
        cmd = PowerCommand()
        result = cmd.execute(2, -1)
        assert result == 0.5
        
        result = cmd.execute(2, -2)
        assert result == 0.25

class TestCommandsWithRandomData:
    """Tests for commands using random data."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Clear history before each test
        Calculator.clear_history()
    
    def test_arithmetic_commands_random(self, faker, num_records):
        """Test arithmetic commands with random data, skipping invalid math domains but asserting correctness for valid cases."""
        for i in range(num_records):
            num1 = faker.pyfloat(min_value=-100, max_value=100, right_digits=2)
            num2 = faker.pyfloat(min_value=-100, max_value=100, right_digits=2)
            if abs(num2) < 0.001:
                num2 = 1.0
            # Test add
            add_cmd = AddCommand()
            add_result = add_cmd.execute(num1, num2)
            assert math.isclose(add_result, num1 + num2, rel_tol=1e-9)
            # Test subtract
            sub_cmd = SubtractCommand()
            sub_result = sub_cmd.execute(num1, num2)
            assert math.isclose(sub_result, num1 - num2, rel_tol=1e-9)
            # Test multiply
            mul_cmd = MultiplyCommand()
            mul_result = mul_cmd.execute(num1, num2)
            assert math.isclose(mul_result, num1 * num2, rel_tol=1e-9)
            # Test divide
            div_cmd = DivideCommand()
            try:
                div_result = div_cmd.execute(num1, num2)
                assert math.isclose(div_result, num1 / num2, rel_tol=1e-9)
            except ZeroDivisionError:
                pass
            # Test power
            power_cmd = PowerCommand()
            limited_num2 = min(max(num2, -5), 5)
            try:
                power_result = power_cmd.execute(num1, limited_num2)
                expected_power = num1 ** limited_num2
                if isinstance(power_result, complex) or isinstance(expected_power, complex):
                    continue
                if math.isnan(power_result) and math.isnan(expected_power):
                    assert True
                elif math.isinf(power_result) and math.isinf(expected_power):
                    assert True
                else:
                    assert math.isclose(power_result, expected_power, rel_tol=1e-9, abs_tol=1e-9)
            except (OverflowError, ValueError, TypeError):
                pass
    
    def test_single_arg_commands_random(self, faker, num_records):
        """Test single argument commands with random data."""
        # Get commands
        abs_cmd = AbsoluteCommand()
        sqrt_cmd = SquareRootCommand()
        exp_cmd = ExponentialCommand()
        log_cmd = LogCommand()
        
        # Test with multiple sets of random inputs
        for i in range(num_records):
            # Generate random number
            num = faker.pyfloat(min_value=-50, max_value=50, right_digits=2)
            
            # Test abs command
            abs_result = abs_cmd.execute(num)
            assert math.isclose(abs_result, abs(num), rel_tol=1e-9)
            
            # Test sqrt command (only for positive numbers)
            if num > 0:
                sqrt_result = sqrt_cmd.execute(num)
                assert math.isclose(sqrt_result, math.sqrt(num), rel_tol=1e-9)
            
            # Test exp command
            exp_result = exp_cmd.execute(num)
            assert math.isclose(exp_result, math.exp(num), rel_tol=1e-9)
            
            # Test log command (only for positive numbers)
            if num > 0:
                log_result = log_cmd.execute(num)
                assert math.isclose(log_result, math.log(num), rel_tol=1e-9)
    
    def test_statistical_commands_random(self, faker, num_records):
        """Test statistical commands with random data."""
        # Get commands
        max_cmd = MaxCommand()
        min_cmd = MinCommand()
        mean_cmd = MeanCommand()
        median_cmd = MedianCommand()
        mode_cmd = ModeCommand()
        stdev_cmd = StandardDeviationCommand()
        
        # Test with multiple sets of random inputs
        for i in range(num_records):
            # Generate random list of numbers
            nums = [faker.pyfloat(min_value=-100, max_value=100, right_digits=2) for _ in range(5)]
            
            # Test max command
            max_result = max_cmd.execute(*nums)
            assert math.isclose(max_result, max(nums), rel_tol=1e-9)
            
            # Test min command
            min_result = min_cmd.execute(*nums)
            assert math.isclose(min_result, min(nums), rel_tol=1e-9)
            
            # Test mean command
            mean_result = mean_cmd.execute(*nums)
            assert math.isclose(mean_result, sum(nums) / len(nums), rel_tol=1e-9)
            
            # Test median command
            median_result = median_cmd.execute(*nums)
            sorted_nums = sorted(nums)
            expected_median = (sorted_nums[len(sorted_nums)//2 - 1] + sorted_nums[len(sorted_nums)//2]) / 2 if len(sorted_nums) % 2 == 0 else sorted_nums[len(sorted_nums)//2]
            assert math.isclose(median_result, expected_median, rel_tol=1e-9)
            
            # Test mode command (using a list with a clear mode)
            mode_nums = nums + [nums[0]] * 3  # Add multiple copies of first element to ensure it's the mode
            mode_result = mode_cmd.execute(*mode_nums)
            assert math.isclose(mode_result, nums[0], rel_tol=1e-9)
            
            # Test standard deviation command
            stdev_result = stdev_cmd.execute(*nums)
            # Calculate expected standard deviation
            mean = sum(nums) / len(nums)
            variance = sum((x - mean) ** 2 for x in nums) / (len(nums) - 1)
            expected_stdev = math.sqrt(variance)
            assert math.isclose(stdev_result, expected_stdev, rel_tol=1e-9)
