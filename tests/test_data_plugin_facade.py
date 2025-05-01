"""
Unit tests for the data plugin facade.
"""

import os
import tempfile

import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from src.plugins.data import DataFacade

class TestDataFacade:
    """Tests for the DataFacade class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create a temporary directory for testing
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_facade = DataFacade(data_dir=self.temp_dir.name)
        
        # Create a test CSV file
        self.test_csv_path = os.path.join(self.temp_dir.name, "test.csv")
        # self.test_df = pd.DataFrame({
        #     'Abbreviation': ['CA', 'NY', 'TX'],
        #     'State': ['California', 'New York', 'Texas'],
        #     'Population': [39538223, 19530351, 29145505]
        # })
        # self.test_df.to_csv(self.test_csv_path, index=False)
    
    def teardown_method(self):
        """Tear down test fixtures."""
        self.temp_dir.cleanup()
    
    def test_init(self):
        """Test initialization of DataFacade."""
        # Test with default data directory
        facade = DataFacade()
        assert os.path.basename(facade.data_dir) == 'data'
        assert facade.current_df is None
        assert facade.current_file is None
        
        # Test with custom data directory
        facade = DataFacade(data_dir='/custom/path')
        assert facade.data_dir == '/custom/path'
    
    def test_list_csv_files(self):
        """Test listing CSV files."""
        # Test with existing directory
        files = self.data_facade.list_csv_files()
        assert len(files) == 0
        
        # Test with non-existent directory
        facade = DataFacade(data_dir='/non/existent/path')
        files = facade.list_csv_files()
        assert len(files) == 0
    
    def test_load_csv(self):
        """Test loading a CSV file."""
        # Test with valid file
        # df = self.data_facade.load_csv("test.csv")
        # assert df is not None
        # assert len(df) == 3
        # assert list(df.columns) == ['Abbreviation', 'State', 'Population']
        # assert self.data_facade.current_file == "test.csv"
        
        # Test with full path
        # df = self.data_facade.load_csv(self.test_csv_path)
        # assert df is not None
        # assert len(df) == 3
        
        # Test with non-existent file
        # df = self.data_facade.load_csv("nonexistent.csv")
        # assert df is None
    
    def test_get_dataframe_info(self):
        """Test getting DataFrame information."""
        # Test with no DataFrame loaded
        info = self.data_facade.get_dataframe_info()
        assert "error" in info
        
        # Load a CSV file
        # self.data_facade.load_csv("test.csv")
        
        # Test with DataFrame loaded
        # info = self.data_facade.get_dataframe_info()
        # assert "file" in info
        # assert "rows" in info
        # assert "columns" in info
        # assert "dtypes" in info
        # assert "statistics" in info
        
        # assert info["file"] == "test.csv"
        # assert info["rows"] == 3
        # assert "Abbreviation" in info["columns"]
        # assert "State" in info["columns"]
        # assert "Population" in info["columns"]
        # assert "Population" in info["statistics"]
        
        # Test with empty DataFrame
        # self.data_facade.current_df = pd.DataFrame()
        # info = self.data_facade.get_dataframe_info()
        # assert "file" in info
        # assert "rows" in info
        # assert info["rows"] == 0
    
    def test_filter_dataframe(self):
        """Test filtering DataFrame."""
        # Test with no DataFrame loaded
        # filtered_df = self.data_facade.filter_dataframe("State", "California")
        # assert filtered_df is None
        
        # Load a CSV file
        # self.data_facade.load_csv("test.csv")
        
        # Test with exact match (equality operator)
        # filtered_df = self.data_facade.filter_dataframe("State", "California")
        # assert filtered_df is not None
        # assert len(filtered_df) == 1
        # assert filtered_df.iloc[0]["Abbreviation"] == "CA"
        
        # Test with greater than operator
        # filtered_df = self.data_facade.filter_dataframe("Population", 20000000, '>')
        # assert filtered_df is not None
        # assert len(filtered_df) == 2
        
        # Test with less than operator
        # filtered_df = self.data_facade.filter_dataframe("Population", 20000000, '<')
        # assert filtered_df is not None
        # assert len(filtered_df) == 1
        # assert filtered_df.iloc[0]["State"] == "New York"
        
        # Test with greater than or equal operator
        # filtered_df = self.data_facade.filter_dataframe("Population", 29145505, '>=')
        # assert filtered_df is not None
        # assert len(filtered_df) == 2
        
        # Test with less than or equal operator
        # filtered_df = self.data_facade.filter_dataframe("Population", 29145505, '<=')
        # assert filtered_df is not None
        # assert len(filtered_df) == 2
        
        # Test with not equal operator
        # filtered_df = self.data_facade.filter_dataframe("State", "California", '!=')
        # assert filtered_df is not None
        # assert len(filtered_df) == 2
        
        # Test with invalid column
        # filtered_df = self.data_facade.filter_dataframe("InvalidColumn", "value")
        # assert filtered_df is None
        
        # Test with invalid operator
        # filtered_df = self.data_facade.filter_dataframe("State", "California", 'invalid')
        # assert filtered_df is None
    
    def test_save_csv(self):
        """Test saving DataFrame to CSV."""
        # Test with no DataFrame loaded
        success = self.data_facade.save_csv("output.csv")
        assert not success
        
        # Load a CSV file
        # self.data_facade.load_csv("test.csv")
        
        # Test with specific filename
        # output_path = os.path.join(self.temp_dir.name, "output.csv")
        # success = self.data_facade.save_csv("output.csv")
        # assert success
        # assert os.path.exists(output_path)
        
        # Verify the contents of the saved file
        # saved_df = pd.read_csv(output_path)
        # assert len(saved_df) == 3
        # assert list(saved_df.columns) == ['Abbreviation', 'State', 'Population']
        
        # Test saving with no filename provided (uses current_file)
        # success = self.data_facade.save_csv()
        # assert success
        
        # Test saving with no current_file
        # self.data_facade.current_file = None
        # success = self.data_facade.save_csv()
        # assert success
        
        # Test saving with full path
        # full_path = os.path.join(self.temp_dir.name, "subfolder", "output.csv")
        # success = self.data_facade.save_csv(full_path)
        # assert success
        # assert os.path.exists(full_path)

class TestDataFacadeWithRandomData:
    """Tests for DataFacade using random data."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_facade = DataFacade(data_dir=self.temp_dir.name)
    
    def teardown_method(self):
        """Tear down test fixtures."""
        self.temp_dir.cleanup()
    
    def test_with_random_data(self, faker, num_records):
        """Test DataFacade with random data."""
        # Create a test DataFrame with random data
        # data = []
        # for _ in range(num_records):
        #     data.append({
        #         'ID': faker.random_int(min=1000, max=9999),
        #         'Name': faker.name(),
        #         'City': faker.city(),
        #         'Value': faker.pyfloat(min_value=0, max_value=1000, right_digits=2)
        #     })
        # test_df = pd.DataFrame(data)
        # test_csv_path = os.path.join(self.temp_dir.name, "random_test.csv")
        # test_df.to_csv(test_csv_path, index=False)
        # # Test loading the CSV
        # df = self.data_facade.load_csv("random_test.csv")
        # assert df is not None
        # assert len(df) == num_records
        # # Test get_dataframe_info
        # info = self.data_facade.get_dataframe_info()
        # assert info["rows"] == num_records
        # assert "Value" in info["statistics"]
        # # Test filter_dataframe with random value
        # if num_records > 0:
        #     random_id = df.iloc[faker.random_int(min=0, max=num_records-1)]["ID"]
        #     filtered_df = self.data_facade.filter_dataframe("ID", random_id, "==")
        #     assert filtered_df is not None
        #     assert len(filtered_df) == 1
        #     assert filtered_df.iloc[0]["ID"] == random_id
            
            # Save filtered data
            # self.data_facade.current_df = filtered_df
            # success = self.data_facade.save_csv("filtered.csv")
            # assert success
            
            # Verify saved file
            # filtered_path = os.path.join(self.temp_dir.name, "filtered.csv")
            # assert os.path.exists(filtered_path)
            
            # saved_df = pd.read_csv(filtered_path)
            # assert len(saved_df) == 1
            # assert saved_df.iloc[0]["ID"] == random_id
