"""
Extended test coverage for the HistoryDataManager class.
Focuses on methods that are not adequately covered by existing tests.
"""

import pytest
import os
import tempfile
import pandas as pd
from src.calculator import Calculator, Calculation
from src.history.data_manager import HistoryDataManager
from unittest.mock import patch, MagicMock


class TestHistoryDataManagerExtended:
    """Extended tests for HistoryDataManager class to improve coverage."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create a temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_file = os.path.join(self.temp_dir.name, "test_history.csv")
        
        # Create manager for testing
        self.manager = HistoryDataManager(self.test_file)
    
    def teardown_method(self):
        """Tear down test fixtures."""
        # Clean up temporary directory
        self.temp_dir.cleanup()
    
    def test_ensure_data_dir(self):
        """Test _ensure_data_dir method."""
        # Create a nested directory path
        nested_dir = os.path.join(self.temp_dir.name, "nested", "dirs")
        test_file = os.path.join(nested_dir, "history.csv")
        
        # Initialize manager with nested path
        manager = HistoryDataManager(test_file)
        
        # Directory should be created
        assert os.path.exists(nested_dir)
    
    def test_save_calculations_empty_list(self):
        """Test save_calculations with empty list."""
        # Save empty list
        self.manager.save_calculations([])
        
        # Dataframe should remain empty
        assert len(self.manager.df) == 0
    
    def test_filter_history(self):
        """Test filter_history method."""
        # Add some test calculations
        calc1 = Calculation("add", 2, 3, 5)
        calc2 = Calculation("add", 10, 5, 15)
        calc3 = Calculation("multiply", 4, 5, 20)
        
        self.manager.save_calculation(calc1)
        self.manager.save_calculation(calc2)
        self.manager.save_calculation(calc3)
        
        # Filter by operation
        result = self.manager.filter_history(operation="add")
        assert len(result) == 2
        
        # Filter by result
        result = self.manager.filter_history(result=15)
        assert len(result) == 1
        
        # Filter by multiple criteria
        result = self.manager.filter_history(operation="add", num1=2)
        assert len(result) == 1
        
        # Filter with no matches
        result = self.manager.filter_history(operation="divide")
        assert len(result) == 0
    
    def test_to_dict_from_dict(self):
        """Test to_dict and from_dict methods."""
        # Add some test calculations
        calc1 = Calculation("add", 2, 3, 5)
        calc2 = Calculation("multiply", 4, 5, 20)
        
        self.manager.save_calculation(calc1)
        self.manager.save_calculation(calc2)
        
        # Convert to dict
        dict_data = self.manager.to_dict()
        assert len(dict_data) == 2
        
        # Clear and verify empty
        self.manager.clear_history()
        assert len(self.manager.df) == 0
        
        # Restore from dict
        self.manager.from_dict(dict_data)
        assert len(self.manager.df) == 2
    
    def test_get_statistics_empty(self):
        """Test get_statistics with empty dataframe."""
        # Empty dataframe should return empty dict
        stats = self.manager.get_statistics()
        assert stats == {}
    
    def test_get_statistics_with_data(self):
        """Test get_statistics with data."""
        # Add some test calculations
        self.manager.save_calculation(Calculation("add", 2, 3, 5))
        self.manager.save_calculation(Calculation("add", 10, 5, 15))
        self.manager.save_calculation(Calculation("multiply", 4, 5, 20))
        
        # Get statistics
        stats = self.manager.get_statistics()
        
        # Verify statistics
        assert 'operation_counts' in stats
        assert 'add' in stats['operation_counts']
        assert stats['operation_counts']['add'] == 2
        assert 'multiply' in stats['operation_counts']
        assert stats['operation_counts']['multiply'] == 1
        
        assert 'avg_result' in stats
        assert stats['avg_result'] == pytest.approx((5 + 15 + 20) / 3)
        
        assert 'min_result' in stats
        assert stats['min_result'] == 5
        
        assert 'max_result' in stats
        assert stats['max_result'] == 20
        
        assert 'total_calculations' in stats
        assert stats['total_calculations'] == 3
    
    def test_load_history_with_error(self):
        """Test load_history with file error."""
        # Attempt to load from non-existent file
        self.manager.load_history("nonexistent.csv")
        
        # Should create an empty dataframe
        assert isinstance(self.manager.df, pd.DataFrame)
        assert len(self.manager.df) == 0
    
    def test_remove_last_calculation_empty(self):
        """Test remove_last_calculation with empty history."""
        # Should return False
        assert not self.manager.remove_last_calculation()
    
    def test_save_to_csv_error(self):
        """Test _save_to_csv with error handling."""
        # Create a read-only directory that will cause permission errors
        if os.name == 'nt':  # Windows
            readonly_dir = os.path.join(self.temp_dir.name, "readonly")
            os.makedirs(readonly_dir, exist_ok=True)
            readonly_file = os.path.join(readonly_dir, "readonly.csv")
            
            # Create the file first
            with open(readonly_file, 'w') as f:
                f.write("dummy")
            
            # Try to make it read-only - this is best effort on Windows
            os.chmod(readonly_file, 0o444)
            
            # Create manager with read-only file
            manager = HistoryDataManager(readonly_file)
            
            # Add calculation and attempt to save
            manager.save_calculation(Calculation("add", 2, 3, 5))
            
            # Should not raise exception
            assert True  # If we got here, no exception was raised
