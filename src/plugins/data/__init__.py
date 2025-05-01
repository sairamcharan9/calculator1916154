"""
Data plugin for CSV processing.
Implements the Facade pattern for Pandas operations.
"""

import os
import pandas as pd
import logging
from datetime import datetime
from src.commands.command_base import Command
from src.calculator import Calculation

# Get logger
logger = logging.getLogger('calculator.plugins.data')

class DataFacade:
    """
    Facade for Pandas data operations.
    Simplifies interaction with pandas DataFrame objects.
    """
    
    def __init__(self, data_dir=None):
        """
        Initialize the data facade.
        
        Args:
            data_dir (str, optional): Directory containing CSV files
        """
        self.data_dir = data_dir or os.path.join(os.getcwd(), 'data')
        self.current_df = None
        self.current_file = None
        logger.info(f"DataFacade initialized with directory: {self.data_dir}")
    
    def list_csv_files(self):
        """
        List all CSV files in the data directory.
        
        Returns:
            list: List of CSV filenames
        """
        try:
            if not os.path.exists(self.data_dir):
                logger.warning(f"Data directory not found: {self.data_dir}")
                return []
            
            files = [f for f in os.listdir(self.data_dir) if f.endswith('.csv')]
            logger.info(f"Found {len(files)} CSV files in {self.data_dir}")
            return files
        except Exception as e:
            logger.error(f"Error listing CSV files: {e}")
            return []
    
    def load_csv(self, filename):
        """
        Load a CSV file into a pandas DataFrame.
        
        Args:
            filename (str): Name of the CSV file
            
        Returns:
            DataFrame or None: Loaded DataFrame or None if error
        """
        try:
            # Check if file has path, if not add data_dir
            if not os.path.dirname(filename):
                file_path = os.path.join(self.data_dir, filename)
            else:
                file_path = filename
            
            # Check if file exists
            if not os.path.exists(file_path):
                logger.error(f"CSV file not found: {file_path}")
                return None
            
            # Load CSV
            self.current_df = pd.read_csv(file_path)
            self.current_file = filename
            
            logger.info(f"Loaded CSV file: {filename} with {len(self.current_df)} rows")
            return self.current_df
        except Exception as e:
            logger.error(f"Error loading CSV file {filename}: {e}")
            return None
    
    def get_dataframe_info(self):
        """
        Get information about the current DataFrame.
        
        Returns:
            dict: DataFrame information
        """
        if self.current_df is None:
            logger.warning("No DataFrame loaded")
            return {"error": "No DataFrame loaded"}
        
        try:
            info = {
                "file": self.current_file,
                "rows": len(self.current_df),
                "columns": list(self.current_df.columns),
                "dtypes": {col: str(dtype) for col, dtype in self.current_df.dtypes.items()}
            }
            
            # Add basic statistics if numeric columns exist
            numeric_cols = self.current_df.select_dtypes(include=['number']).columns
            if len(numeric_cols) > 0:
                info["statistics"] = {
                    col: {
                        "mean": self.current_df[col].mean(),
                        "min": self.current_df[col].min(),
                        "max": self.current_df[col].max()
                    } for col in numeric_cols
                }
            
            logger.info(f"Generated info for DataFrame with {len(self.current_df)} rows")
            return info
        except Exception as e:
            logger.error(f"Error getting DataFrame info: {e}")
            return {"error": str(e)}
    
    def filter_dataframe(self, column, value, operator='=='):
        """
        Filter the current DataFrame by column and value.
        
        Args:
            column (str): Column name to filter on
            value: Value to filter by
            operator (str): Comparison operator ('==', '>', '<', '>=', '<=', '!=')
            
        Returns:
            DataFrame or None: Filtered DataFrame or None if error
        """
        if self.current_df is None:
            logger.warning("No DataFrame loaded")
            return None
        
        try:
            if column not in self.current_df.columns:
                logger.error(f"Column not found: {column}")
                return None
            
            # Only cast to numeric if value is int or float
            if column in self.current_df.columns and isinstance(value, (int, float)):
                try:
                    self.current_df[column] = pd.to_numeric(self.current_df[column], errors='coerce')
                except Exception:
                    pass
            
            # Apply filter based on operator
            if operator == '==':
                filtered_df = self.current_df[self.current_df[column] == value]
            elif operator == '>':
                filtered_df = self.current_df[self.current_df[column] > value]
            elif operator == '<':
                filtered_df = self.current_df[self.current_df[column] < value]
            elif operator == '>=':
                filtered_df = self.current_df[self.current_df[column] >= value]
            elif operator == '<=':
                filtered_df = self.current_df[self.current_df[column] <= value]
            elif operator == '!=':
                filtered_df = self.current_df[self.current_df[column] != value]
            else:
                logger.error(f"Unsupported operator: {operator}")
                return None
            
            logger.info(f"Filtered DataFrame on {column} {operator} {value}, {len(filtered_df)} rows remaining")
            return filtered_df
        except Exception as e:
            logger.error(f"Error filtering DataFrame: {e}")
            return None
    
    def save_csv(self, filename=None):
        """
        Save the current DataFrame to a CSV file.
        
        Args:
            filename (str, optional): Filename to save as, defaults to original filename
            
        Returns:
            bool: True if successful, False otherwise
        """
        if self.current_df is None:
            logger.warning("No DataFrame loaded")
            return False
        
        try:
            # Use original filename if none provided
            if filename is None:
                if self.current_file is None:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"output_{timestamp}.csv"
                else:
                    filename = self.current_file
            
            # Add data directory path if no directory specified
            if not os.path.dirname(filename):
                file_path = os.path.join(self.data_dir, filename)
            else:
                file_path = filename
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            # Save DataFrame
            self.current_df.to_csv(file_path, index=False)
            logger.info(f"Saved DataFrame to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error saving DataFrame: {e}")
            return False


# Create singleton instance
data_facade = DataFacade()


class ListCSVCommand(Command):
    """Command to list all available CSV files."""
    
    @property
    def name(self) -> str:
        return "list_csv"
    
    def execute(self) -> str:
        """
        Execute the list_csv command.
        
        Returns:
            str: List of CSV files
        """
        files = data_facade.list_csv_files()
        if not files:
            return "No CSV files found in the data directory."
        
        result = "Available CSV files:\n"
        for i, file in enumerate(files, 1):
            result += f"{i}. {file}\n"
        
        return result


class LoadCSVCommand(Command):
    """Command to load a CSV file."""
    
    @property
    def name(self) -> str:
        return "load_csv"
    
    def execute(self, filename) -> str:
        """
        Execute the load_csv command.
        
        Args:
            filename (str): Name of the CSV file to load
            
        Returns:
            str: Status message
        """
        df = data_facade.load_csv(filename)
        if df is None:
            return f"Failed to load CSV file: {filename}"
        
        return f"Successfully loaded {filename} with {len(df)} rows and {len(df.columns)} columns."


class DataInfoCommand(Command):
    """Command to get information about the current DataFrame."""
    
    @property
    def name(self) -> str:
        return "data_info"
    
    def execute(self) -> str:
        """
        Execute the data_info command.
        
        Returns:
            str: DataFrame information
        """
        info = data_facade.get_dataframe_info()
        if "error" in info:
            return f"Error: {info['error']}"
        
        result = f"File: {info['file']}\n"
        result += f"Rows: {info['rows']}\n"
        result += f"Columns: {', '.join(info['columns'])}\n"
        
        if "statistics" in info:
            result += "\nStatistics:\n"
            for col, stats in info["statistics"].items():
                result += f"  {col}:\n"
                result += f"    Mean: {stats['mean']}\n"
                result += f"    Min: {stats['min']}\n"
                result += f"    Max: {stats['max']}\n"
        
        return result


class FilterDataCommand(Command):
    """Command to filter the current DataFrame."""
    
    @property
    def name(self) -> str:
        return "filter"
    
    def execute(self, column, value, operator="==") -> str:
        """
        Execute the filter command.
        
        Args:
            column (str): Column name to filter on
            value: Value to filter by
            operator (str, optional): Comparison operator ('==', '>', '<', '>=', '<=', '!=')
            
        Returns:
            str: Status message
        """
        # Defensive: check if DataFrame is loaded
        if data_facade.current_df is None:
            return "No DataFrame loaded. Load a CSV file first."
        
        # Ensure value is cast to the column dtype for comparison
        if column in data_facade.current_df.columns:
            col_dtype = data_facade.current_df[column].dtype
            try:
                value = col_dtype.type(value)
            except Exception:
                pass
        filtered_df = data_facade.filter_dataframe(column, value, operator)
        if filtered_df is None:
            return "Failed to filter DataFrame."
        
        # Update current DataFrame
        data_facade.current_df = filtered_df
        
        return f"DataFrame filtered on {column} {operator} {value}. {len(filtered_df)} rows remaining."


class SortCommand(Command):
    """Command to sort the current DataFrame."""
    
    @property
    def name(self) -> str:
        return "sort"
    
    def execute(self, column, ascending=True) -> str:
        """
        Execute the sort command.
        
        Args:
            column (str): Column name to sort by
            ascending (bool, optional): Sort in ascending order (default) or descending
            
        Returns:
            str: Status message
        """
        if data_facade.current_df is None:
            return "No DataFrame loaded. Load a CSV file first."
        
        try:
            data_facade.current_df = data_facade.current_df.sort_values(by=column, ascending=ascending)
            direction = "ascending" if ascending else "descending"
            logger.info(f"DataFrame sorted by {column} in {direction} order")
            return f"DataFrame sorted by {column} in {direction} order."
        except Exception as e:
            logger.error(f"Error sorting DataFrame: {e}")
            return f"Error sorting DataFrame: {e}"


class StatisticsCommand(Command):
    """Command to calculate statistics on the current DataFrame."""
    
    @property
    def name(self) -> str:
        return "statistics"
    
    def execute(self, column=None) -> str:
        """
        Execute the statistics command.
        
        Args:
            column (str, optional): Column name to calculate statistics for.
                                    If None, statistics are calculated for all numeric columns.
            
        Returns:
            str: Statistics summary
        """
        if data_facade.current_df is None:
            return "No DataFrame loaded. Load a CSV file first."
        
        try:
            if column:
                if column not in data_facade.current_df.columns:
                    return f"Column '{column}' not found in DataFrame."
                
                # Check if column is numeric
                if not pd.api.types.is_numeric_dtype(data_facade.current_df[column]):
                    return f"Column '{column}' is not numeric. Statistics can only be calculated for numeric columns."
                
                # Calculate statistics for the specified column
                stats = data_facade.current_df[column].describe()
                return f"Statistics for column '{column}':\n{stats}"
            else:
                # Calculate statistics for all numeric columns
                numeric_cols = data_facade.current_df.select_dtypes(include=["number"]).columns
                if len(numeric_cols) == 0:
                    return "No numeric columns found in DataFrame."
                
                stats = data_facade.current_df[numeric_cols].describe()
                return f"Statistics for all numeric columns:\n{stats}"
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return f"Error calculating statistics: {e}"


class SaveCSVCommand(Command):
    """Command to save the current DataFrame to a CSV file."""
    
    @property
    def name(self) -> str:
        return "save_csv"
    
    def execute(self, filename=None) -> str:
        """
        Execute the save_csv command.
        
        Args:
            filename (str, optional): Filename to save as
            
        Returns:
            str: Status message
        """
        success = data_facade.save_csv(filename)
        if not success:
            return "Failed to save DataFrame."
        
        return f"DataFrame saved to {filename or data_facade.current_file}."


class MaxCommand(Command):
    """Command to calculate the maximum of a set of numbers."""
    
    @property
    def name(self) -> str:
        return "max"
    
    def execute(self, *args) -> float:
        """
        Execute maximum operation.
        
        Args:
            *args: Numbers to find maximum of
            
        Returns:
            float: Maximum value
            
        Raises:
            ValueError: If no arguments are provided
        """
        if not args:
            raise ValueError("At least one number is required")
        
        result = max(args)
        # Add to history with first number as main and others as optional
        Calculation("max", args[0], args[1:], result)
        logger.info(f"Maximum operation executed: max{args} = {result}")
        return result

class MinCommand(Command):
    """Command to calculate the minimum of a set of numbers."""
    
    @property
    def name(self) -> str:
        return "min"
    
    def execute(self, *args) -> float:
        """
        Execute minimum operation.
        
        Args:
            *args: Numbers to find minimum of
            
        Returns:
            float: Minimum value
            
        Raises:
            ValueError: If no arguments are provided
        """
        if not args:
            raise ValueError("At least one number is required")
        
        result = min(args)
        # Add to history with first number as main and others as optional
        Calculation("min", args[0], args[1:], result)
        logger.info(f"Minimum operation executed: min{args} = {result}")
        return result

class MeanCommand(Command):
    """Command to calculate the arithmetic mean of a set of numbers."""
    
    @property
    def name(self) -> str:
        return "mean"
    
    def execute(self, *args) -> float:
        """
        Execute mean operation.
        
        Args:
            *args: Numbers to find mean of
            
        Returns:
            float: Mean value
            
        Raises:
            ValueError: If no arguments are provided
        """
        if not args:
            raise ValueError("At least one number is required")
        
        result = sum(args) / len(args)
        # Add to history with first number as main and others as optional
        Calculation("mean", args[0], args[1:], result)
        logger.info(f"Mean operation executed: mean{args} = {result}")
        return result

class MedianCommand(Command):
    """Command to calculate the median of a set of numbers."""
    
    @property
    def name(self) -> str:
        return "median"
    
    def execute(self, *args) -> float:
        """
        Execute median operation.
        
        Args:
            *args: Numbers to find median of
            
        Returns:
            float: Median value
            
        Raises:
            ValueError: If no arguments are provided
        """
        if not args:
            raise ValueError("At least one number is required")
        
        sorted_args = sorted(args)
        n = len(sorted_args)
        
        if n % 2 == 0:
            # Even number of elements, take average of middle two
            result = (sorted_args[n//2 - 1] + sorted_args[n//2]) / 2
        else:
            # Odd number of elements, take middle one
            result = sorted_args[n//2]
            
        # Add to history with first number as main and others as optional
        Calculation("median", args[0], args[1:], result)
        logger.info(f"Median operation executed: median{args} = {result}")
        return result

class ModeCommand(Command):
    """Command to calculate the mode of a set of numbers."""
    
    @property
    def name(self) -> str:
        return "mode"
    
    def execute(self, *args) -> float:
        """
        Execute mode operation.
        
        Args:
            *args: Numbers to find mode of
            
        Returns:
            float: Mode value (first mode if multiple)
            
        Raises:
            ValueError: If no arguments are provided
        """
        if not args:
            raise ValueError("At least one number is required")
        
        # Count occurrences of each number
        count_dict = {}
        for num in args:
            count_dict[num] = count_dict.get(num, 0) + 1
            
        # Find the most common number(s)
        max_count = max(count_dict.values())
        modes = [num for num, count in count_dict.items() if count == max_count]
        
        # Return the first mode
        result = modes[0]
        # Add to history with first number as main and others as optional
        Calculation("mode", args[0], args[1:], result)
        logger.info(f"Mode operation executed: mode{args} = {result}")
        return result

class StandardDeviationCommand(Command):
    """Command to calculate the standard deviation of a set of numbers."""
    
    @property
    def name(self) -> str:
        return "stdev"
    
    def execute(self, *args) -> float:
        """
        Execute standard deviation operation.
        
        Args:
            *args: Numbers to find standard deviation of
            
        Returns:
            float: Standard deviation value
            
        Raises:
            ValueError: If fewer than two arguments are provided
        """
        if len(args) < 2:
            raise ValueError("At least two numbers are required for standard deviation")
        
        # Calculate mean
        mean = sum(args) / len(args)
        
        # Calculate sum of squared differences from mean
        sum_squared_diff = sum((x - mean) ** 2 for x in args)
        
        # Calculate standard deviation
        result = (sum_squared_diff / (len(args) - 1)) ** 0.5
            
        # Add to history with first number as main and others as optional
        Calculation("stdev", args[0], args[1:], result)
        logger.info(f"Standard deviation operation executed: stdev{args} = {result}")
        return result

# Plugin registry for dynamic discovery
PLUGIN_REGISTRY = {}

def register_commands(command_registry):
    """
    Register data commands to the global command registry.
    
    Args:
        command_registry (dict): The global command registry
    """
    # Create command instances
    data_commands = [
        ListCSVCommand(),
        LoadCSVCommand(),
        DataInfoCommand(),
        FilterDataCommand(),
        SortCommand(),
        StatisticsCommand(),
        SaveCSVCommand(),
        MaxCommand(),
        MinCommand(),
        MeanCommand(),
        MedianCommand(),
        ModeCommand(),
        StandardDeviationCommand()
    ]
    
    # Register each command
    for cmd in data_commands:
        command_registry[cmd.name] = cmd
        logger.info(f"Registered data command: {cmd.name}")
    
    return [cmd.name for cmd in data_commands]
