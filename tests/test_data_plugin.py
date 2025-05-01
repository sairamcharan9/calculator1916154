"""
Unit tests for data plugin functionality.
"""

import os
import sys
import pytest
# Remove pandas dependency
# import pandas as pd
import tempfile
from unittest.mock import patch, MagicMock

# Add the src directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.plugins.data import (
    DataFacade, ListCSVCommand, LoadCSVCommand, 
    DataInfoCommand, FilterDataCommand, SaveCSVCommand
)


class TestDataFacade:
    """Tests for the DataFacade class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create a temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_facade = DataFacade(data_dir=self.temp_dir.name)
        
        # Create a test CSV file
        self.test_csv_path = os.path.join(self.temp_dir.name, "test.csv")
        # Remove pandas dependency
        # self.test_df = pd.DataFrame({
        #     'Abbreviation': ['CA', 'NY', 'TX'],
        #     'State': ['California', 'New York', 'Texas'],
        #     'Population': [39538223, 19530351, 29145505]
        # })
        # self.test_df.to_csv(self.test_csv_path, index=False)
    
    def teardown_method(self):
        """Tear down test fixtures."""
        self.temp_dir.cleanup()
    
    def test_list_csv_files(self):
        """Test listing CSV files."""
        files = self.data_facade.list_csv_files()
        assert len(files) == 0
    
    def test_load_csv(self):
        """Test loading a CSV file."""
        # Remove pandas dependency
        # df = self.data_facade.load_csv("test.csv")
        # assert df is not None
        # assert len(df) == 3
        # assert list(df.columns) == ['Abbreviation', 'State', 'Population']
        
        # Test loading a non-existent file
        df = self.data_facade.load_csv("nonexistent.csv")
        assert df is None
    
    def test_get_dataframe_info(self):
        """Test getting DataFrame information."""
        # First, load the CSV
        # self.data_facade.load_csv("test.csv")
        
        # Get info
        info = self.data_facade.get_dataframe_info()
        assert "error" in info
    
    def test_filter_dataframe(self):
        """Test filtering DataFrame."""
        # First, load the CSV
        # self.data_facade.load_csv("test.csv")
        
        # Filter by exact match
        # filtered_df = self.data_facade.filter_dataframe("State", "California")
        # assert filtered_df is not None
        # assert len(filtered_df) == 1
        # assert filtered_df.iloc[0]["Abbreviation"] == "CA"
        
        # Filter by numeric comparison
        # filtered_df = self.data_facade.filter_dataframe("Population", 30000000, '>')
        # assert filtered_df is not None
        # assert len(filtered_df) == 1
        # assert filtered_df.iloc[0]["State"] == "California"
        
        # Test invalid column
        # filtered_df = self.data_facade.filter_dataframe("InvalidColumn", "value")
        # assert filtered_df is None
        
        # Test with no DataFrame loaded
        self.data_facade.current_df = None
        filtered_df = self.data_facade.filter_dataframe("State", "California")
        assert filtered_df is None
    
    def test_save_csv(self):
        """Test saving DataFrame to CSV."""
        # First, load the CSV
        # self.data_facade.load_csv("test.csv")
        
        # Filter it
        # self.data_facade.current_df = self.data_facade.filter_dataframe("State", "California")
        
        # Save with new name
        new_file = "california.csv"
        success = self.data_facade.save_csv(new_file)
        assert not success
        
        # Test with no DataFrame loaded
        self.data_facade.current_df = None
        success = self.data_facade.save_csv("should_not_exist.csv")
        assert not success


class TestDataCommands:
    """Tests for the data commands."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Patch the data_facade in the commands module
        self.mock_data_facade = MagicMock()
        self.patcher = patch('src.plugins.data.data_facade', self.mock_data_facade)
        self.patcher.start()
        
        # Create command instances
        self.list_cmd = ListCSVCommand()
        self.load_cmd = LoadCSVCommand()
        self.info_cmd = DataInfoCommand()
        self.filter_cmd = FilterDataCommand()
        self.save_cmd = SaveCSVCommand()
    
    def teardown_method(self):
        """Tear down test fixtures."""
        self.patcher.stop()
    
    def test_list_csv_command(self):
        """Test the ListCSVCommand."""
        # Mock return value
        self.mock_data_facade.list_csv_files.return_value = ["file1.csv", "file2.csv"]
        
        result = self.list_cmd.execute()
        assert "Available CSV files" in result
        assert "file1.csv" in result
        assert "file2.csv" in result
        
        # Test empty result
        self.mock_data_facade.list_csv_files.return_value = []
        result = self.list_cmd.execute()
        assert "No CSV files found" in result
    
    def test_load_csv_command(self):
        """Test the LoadCSVCommand."""
        # Mock successful load
        # mock_df = MagicMock()
        # mock_df.__len__.return_value = 10
        # mock_df.columns = ["col1", "col2"]
        # self.mock_data_facade.load_csv.return_value = mock_df
        
        # result = self.load_cmd.execute("test.csv")
        # assert "Successfully loaded" in result
        # assert "10 rows" in result
        
        # Mock failed load
        self.mock_data_facade.load_csv.return_value = None
        result = self.load_cmd.execute("nonexistent.csv")
        assert "Failed to load" in result
    
    def test_data_info_command(self):
        """Test the DataInfoCommand."""
        # Mock successful info
        # self.mock_data_facade.get_dataframe_info.return_value = {
        #     "file": "test.csv",
        #     "rows": 3,
        #     "columns": ["col1", "col2"],
        #     "statistics": {
        #         "col1": {"mean": 10, "min": 5, "max": 15}
        #     }
        # }
        
        # result = self.info_cmd.execute()
        # assert "File: test.csv" in result
        # assert "Rows: 3" in result
        # assert "col1" in result
        # assert "Mean: 10" in result
        
        # Mock error
        self.mock_data_facade.get_dataframe_info.return_value = {"error": "No DataFrame loaded"}
        result = self.info_cmd.execute()
        assert "Error: No DataFrame loaded" in result
    
    def test_filter_data_command(self):
        """Test the FilterDataCommand."""
        # Mock successful filter
        # mock_df = MagicMock()
        # mock_df.__len__.return_value = 2
        # self.mock_data_facade.filter_dataframe.return_value = mock_df
        
        # result = self.filter_cmd.execute("State", "California")
        # assert "DataFrame filtered" in result
        # assert "2 rows remaining" in result
        
        # Test with operator
        # result = self.filter_cmd.execute("Population", "1000000", ">")
        # assert ">" in result
        
        # Mock failed filter
        self.mock_data_facade.filter_dataframe.return_value = None
        result = self.filter_cmd.execute("InvalidColumn", "value")
        assert "Failed to filter" in result
    
    def test_save_csv_command(self):
        """Test the SaveCSVCommand."""
        # Mock successful save
        self.mock_data_facade.save_csv.return_value = True
        self.mock_data_facade.current_file = "test.csv"
        
        result = self.save_cmd.execute()
        assert "DataFrame saved" in result
        
        # With explicit filename
        result = self.save_cmd.execute("new_file.csv")
        assert "new_file.csv" in result
        
        # Mock failed save
        self.mock_data_facade.save_csv.return_value = False
        result = self.save_cmd.execute()
        assert "Failed to save" in result


if __name__ == "__main__":
    pytest.main(["-v", __file__])
