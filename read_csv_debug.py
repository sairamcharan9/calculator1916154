"""
Debug script to read and print the CSV file created by HistoryDataManager
"""
import os
import pandas as pd
import tempfile
import shutil
from src.calculator import Calculation
from src.history.data_manager import HistoryDataManager

# Create a temporary file for testing
temp_dir = tempfile.mkdtemp()
temp_file = os.path.join(temp_dir, 'test_history.csv')

try:
    # Create a data manager with the temp file
    data_manager = HistoryDataManager(temp_file)
    
    # Create a calculation and save it
    calc = Calculation("mul", 2, 3, 6)
    data_manager.save_calculation(calc)
    
    # Read the raw CSV file
    print(f"Raw CSV content:")
    with open(temp_file, 'r') as file:
        content = file.read()
        print(content)
    
    # Read using pandas to see how it's parsed
    print("\nParsed with pandas:")
    df = pd.read_csv(temp_file)
    print(df)
    
    # Check specific columns
    print("\nResult column value:", df['result'].iloc[0])
    
finally:
    # Clean up
    shutil.rmtree(temp_dir)
