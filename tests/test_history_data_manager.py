"""
Unit tests for the history data manager module.
"""
import os
import tempfile
# import pandas as pd
import pytest
from src.calculator import Calculation
from src.history.data_manager import HistoryDataManager
import shutil

@pytest.fixture
def temp_history_file():
    tmpdir = tempfile.mkdtemp()
    file_path = os.path.join(tmpdir, "history.csv")
    yield file_path
    shutil.rmtree(tmpdir)

@pytest.fixture
def data_manager(temp_history_file):
    return HistoryDataManager(data_file=temp_history_file)

def test_init_and_ensure_data_dir(tmp_path):
    # Should create directory if not exists
    dir_path = tmp_path / "subdir"
    file_path = dir_path / "history.csv"
    assert not dir_path.exists()
    mgr = HistoryDataManager(data_file=str(file_path))
    assert dir_path.exists()
    assert mgr.data_file == str(file_path)

def test_save_single_and_multiple_calculation(data_manager):
    calc1 = Calculation("add", 1, 2, 3)
    calc2 = Calculation("sub", 4, 1, 3)
    data_manager.save_calculation(calc1)
    assert not data_manager.df.empty
    data_manager.save_calculations([calc2])
    assert len(data_manager.df) == 2

def test_save_empty_calculations(data_manager, caplog):
    data_manager.save_calculations([])
    assert "No calculations to save" in caplog.text

def test_save_and_load_csv(data_manager, temp_history_file):
    calc = Calculation("mul", 2, 3, 6)
    data_manager.save_calculation(calc)
    # Now load from file
    with open(temp_history_file, 'r') as file:
        lines = file.readlines()
    
    assert len(lines) > 0
    # Debug: Print the content of the CSV file
    print(f"CSV header: {lines[0].strip()}")
    print(f"CSV data: {lines[1].strip()}")
    csv_values = lines[1].strip().split(',')
    print(f"CSV values: {csv_values}")
    print(f"Result value at index 4: {csv_values[4]}")  # Change from index 3 to 4
    
    # The CSV format includes timestamp first, so result should be at index 4
    assert csv_values[4] == '6'

def test_load_history_missing_file(data_manager):
    # Should not raise error, just log
    data_manager.load_history("does_not_exist.csv")
    assert data_manager.df.empty

def test_clear_and_filter(data_manager):
    calc = Calculation("add", 1, 2, 3)
    data_manager.save_calculation(calc)
    data_manager.clear_history()
    assert data_manager.df.empty
    # Add again for filter test
    data_manager.save_calculation(calc)
    filtered = data_manager.filter_history(operation="add")
    assert len(filtered) == 1
    filtered_none = data_manager.filter_history(operation="sub")
    assert filtered_none.empty

def test_get_history(data_manager):
    calc = Calculation("add", 1, 2, 3)
    data_manager.save_calculation(calc)
    hist = data_manager.get_history()
    assert isinstance(hist, list)
    assert hist[0].operation == "add"

def test_to_dict_and_from_dict(data_manager):
    calc = Calculation("add", 1, 2, 3)
    data_manager.save_calculation(calc)
    dct = data_manager.to_dict()
    assert isinstance(dct, list)
    mgr2 = HistoryDataManager(data_file=data_manager.data_file)
    mgr2.from_dict(dct)
    assert not mgr2.df.empty

def test_edge_cases(data_manager):
    # Save calculation with None values
    calc = Calculation("noop", None, None, None)
    data_manager.save_calculation(calc)
    assert not data_manager.df.empty
    # Try filtering with no matches
    filtered = data_manager.filter_history(operation="nonexistent")
    assert filtered.empty
    # Try loading from malformed file
    with tempfile.NamedTemporaryFile(delete=False, mode="w+") as badfile:
        badfile.write("not,a,valid,csv\n1,2,3\n")
        badfile.close()
        data_manager.load_history(badfile.name)
        # Should not raise, just log
    os.unlink(badfile.name)
