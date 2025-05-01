"""
Unit tests for the data plugin commands.
"""
import os
import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import tempfile

from src.plugins.data import (
    ListCSVCommand, LoadCSVCommand, DataInfoCommand,
    FilterDataCommand, SaveCSVCommand, data_facade
)

class TestDataCommands:
    """Tests for the data plugin commands."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create a temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()

        # Always recreate the test DataFrame and CSV for each test
        self.test_df = pd.DataFrame({
            'Abbreviation': ['CA', 'NY', 'TX'],
            'State': ['California', 'New York', 'Texas'],
            'Population': [39538223, 19530351, 29145505]
        })
        self.test_csv_path = os.path.join(self.temp_dir.name, "test.csv")
        self.test_df.to_csv(self.test_csv_path, index=False)

        # Create commands
        self.list_cmd = ListCSVCommand()
        self.load_cmd = LoadCSVCommand()
        self.info_cmd = DataInfoCommand()
        self.filter_cmd = FilterDataCommand()
        self.save_cmd = SaveCSVCommand()

        # Patch the data_facade methods to use our temporary directory
        self.original_data_dir = data_facade.data_dir
        data_facade.data_dir = self.temp_dir.name
        
    def teardown_method(self):
        """Tear down test fixtures."""
        # Restore the original data directory
        data_facade.data_dir = self.original_data_dir
        data_facade.current_df = None
        data_facade.current_file = None
        
        # Clean up temporary directory
        self.temp_dir.cleanup()
    
    def test_list_csv_command(self):
        """Test ListCSVCommand."""
        # Test with CSV files present
        result = self.list_cmd.execute()
        assert "Available CSV files" in result
        assert "test.csv" in result
        
        # Test with no CSV files
        for file in os.listdir(self.temp_dir.name):
            if file.endswith('.csv'):
                os.remove(os.path.join(self.temp_dir.name, file))
        
        result = self.list_cmd.execute()
        assert "No CSV files found" in result
    
    def test_load_csv_command(self):
        """Test LoadCSVCommand."""
        # Test loading a valid CSV file
        result = self.load_cmd.execute("test.csv")
        assert "Successfully loaded" in result
        assert "3 rows" in result
        assert "3 columns" in result
        
        # Test loading a non-existent CSV file
        result = self.load_cmd.execute("nonexistent.csv")
        assert "Failed to load" in result
    
    def test_data_info_command(self):
        """Test DataInfoCommand."""
        # Test with no DataFrame loaded
        result = self.info_cmd.execute()
        assert "Error" in result
        
        # Load a DataFrame
        self.load_cmd.execute("test.csv")
        
        # Test with DataFrame loaded
        result = self.info_cmd.execute()
        assert "File: test.csv" in result
        assert "Rows: 3" in result
        assert "Columns: Abbreviation, State, Population" in result
        assert "Statistics" in result
        assert "Population" in result
        assert "Mean" in result
        assert "Min" in result
        assert "Max" in result
    
    def test_filter_data_command(self):
        """Test FilterDataCommand."""
        # Load a DataFrame
        self.load_cmd.execute("test.csv")
        
        # Test filtering by exact match
        result = self.filter_cmd.execute("State", "California")
        assert "DataFrame filtered" in result
        assert "1 rows remaining" in result
        
        # Test filtering with operator
        result = self.filter_cmd.execute("Population", "20000000", ">")
        print(f"Filter result: {result}")
        print(f"Current DataFrame after filter:\n{data_facade.current_df}")
        assert "DataFrame filtered" in result
        assert ">" in result
        assert "1 rows remaining" in result
        
        # Test with invalid column
        result = self.filter_cmd.execute("InvalidColumn", "value")
        assert "Failed to filter" in result
        
        # Test with no DataFrame loaded
        data_facade.current_df = None
        result = self.filter_cmd.execute("State", "California")
        assert ("Failed to filter" in result) or ("No DataFrame loaded" in result)
    
    def test_save_csv_command(self):
        """Test SaveCSVCommand."""
        # Test with no DataFrame loaded
        result = self.save_cmd.execute()
        assert "Failed to save" in result
        
        # Load a DataFrame
        self.load_cmd.execute("test.csv")
        
        # Test saving with default filename
        result = self.save_cmd.execute()
        assert "DataFrame saved" in result
        assert "test.csv" in result
        
        # Test saving with specific filename
        result = self.save_cmd.execute("output.csv")
        assert "DataFrame saved" in result
        assert "output.csv" in result
        
        # Verify file was saved
        output_path = os.path.join(self.temp_dir.name, "output.csv")
        assert os.path.exists(output_path)

class TestDataCommandsWithRandomData:
    """Tests for data commands with random data."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create a temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()

        # Always recreate the test DataFrame and CSV for each test
        self.test_df = pd.DataFrame({
            'Abbreviation': ['CA', 'NY', 'TX'],
            'State': ['California', 'New York', 'Texas'],
            'Population': [39538223, 19530351, 29145505]
        })
        self.test_csv_path = os.path.join(self.temp_dir.name, "test.csv")
        self.test_df.to_csv(self.test_csv_path, index=False)

        # Create commands
        self.list_cmd = ListCSVCommand()
        self.load_cmd = LoadCSVCommand()
        self.info_cmd = DataInfoCommand()
        self.filter_cmd = FilterDataCommand()
        self.save_cmd = SaveCSVCommand()

        # Patch the data_facade methods to use our temporary directory
        self.original_data_dir = data_facade.data_dir
        data_facade.data_dir = self.temp_dir.name
    
    def teardown_method(self):
        """Tear down test fixtures."""
        # Restore the original data directory
        data_facade.data_dir = self.original_data_dir
        data_facade.current_df = None
        data_facade.current_file = None
        
        # Clean up temporary directory
        self.temp_dir.cleanup()
    
    def test_with_random_data(self, faker, num_records, csv_data_for_tests):
        """Test data commands with random data."""
        # Get the CSV data from fixture
        csv_path = csv_data_for_tests['files']['states']
        
        # Copy the CSV file to our test directory
        test_df = pd.read_csv(csv_path)
        test_path = os.path.join(self.temp_dir.name, "random_test.csv")
        test_df.to_csv(test_path, index=False)
        
        # Test list_csv command
        result = self.list_cmd.execute()
        assert "random_test.csv" in result
        
        # Test load_csv command
        result = self.load_cmd.execute("random_test.csv")
        assert "Successfully loaded" in result
        assert f"{len(test_df)} rows" in result
        
        # Test data_info command
        result = self.info_cmd.execute()
        assert "File: random_test.csv" in result
        assert f"Rows: {len(test_df)}" in result
        assert "Population" in result
        
        # Test filter_data command with random filters
        if len(test_df) > 0:
            # Get a random state from the DataFrame
            random_state = test_df.iloc[faker.random_int(min=0, max=len(test_df)-1)]["State"]
            
            # Filter by that state
            result = self.filter_cmd.execute("State", random_state)
            assert "DataFrame filtered" in result
            
            # Save filtered data
            result = self.save_cmd.execute("filtered.csv")
            assert "DataFrame saved" in result
            
            # Verify saved file
            filtered_path = os.path.join(self.temp_dir.name, "filtered.csv")
            assert os.path.exists(filtered_path)
            
            # Try different filter operators
            operators = ['>', '<', '>=', '<=', '!=']
            for op in operators:
                random_population = faker.random_int(min=10000, max=40000000)
                result = self.filter_cmd.execute("Population", str(random_population), op)
                if "DataFrame filtered" not in result:
                    print(f"Filter failed: column=Population, value={random_population}, op={op}, result={result}")
                assert "DataFrame filtered" in result
                assert op in result
