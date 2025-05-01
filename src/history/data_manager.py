"""
Data manager for calculator history using Pandas.
Provides save, load, and manipulation functionality for calculation history.
"""

import pandas as pd
import os
from typing import List, Dict, Any, Optional
from src.calculator import Calculation
from src.history.logger import get_logger
from datetime import datetime

logger = get_logger('history')

class HistoryDataManager:
    """
    Manages calculator history data using Pandas.
    Implements the Facade pattern to simplify interaction with Pandas.
    """
    
    def __init__(self, data_file: str = None):
        """
        Initialize history data manager.
        
        Args:
            data_file (str, optional): Path to CSV file for storing history
        """
        self.data_file = data_file or os.getenv('HISTORY_FILE', 'src/history/data/history.csv')
        self._ensure_data_dir()
        self.df = pd.DataFrame(columns=['timestamp', 'operation', 'num1', 'num2', 'result'])
        logger.info(f"Initialized HistoryDataManager with data file: {self.data_file}")
    
    def _ensure_data_dir(self):
        """Ensure the directory for the data file exists."""
        data_dir = os.path.dirname(self.data_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
            logger.info(f"Created data directory: {data_dir}")
    
    def save_calculation(self, calculation: Calculation) -> None:
        """
        Save a calculation to the history dataframe and file.
        
        Args:
            calculation (Calculation): Calculation to save
        """
        # Create a new row for the calculation
        new_row = {
            'timestamp': datetime.now(),
            'operation': calculation.operation,
            'num1': calculation.num1,
            'num2': calculation.num2,
            'result': calculation.result
        }
        # Only append non-empty rows
        new_row_df = pd.DataFrame([new_row])
        if not new_row_df.isna().all(axis=None):
            self.df = pd.concat([self.df, new_row_df], ignore_index=True)
        # Save to CSV
        self._save_to_csv()
        logger.info(f"Saved calculation to history: {calculation}")
    
    def save_calculations(self, calculations: List[Calculation]) -> None:
        """
        Save multiple calculations to history.
        
        Args:
            calculations (List[Calculation]): List of calculations to save
        """
        if not calculations:
            logger.warning("No calculations to save")
            return
        
        # Create new rows for each calculation
        new_rows = []
        for calc in calculations:
            new_rows.append({
                'timestamp': datetime.now(),
                'operation': calc.operation,
                'num1': calc.num1,
                'num2': calc.num2,
                'result': calc.result
            })
        
        # Append to dataframe
        self.df = pd.concat([self.df, pd.DataFrame(new_rows)], ignore_index=True)
        
        # Save to CSV
        self._save_to_csv()
        logger.info(f"Saved {len(calculations)} calculations to history")
    
    def load_history(self, filename=None):
        """Load history from a CSV file (default: self.data_file)."""
        import pandas as pd
        fname = filename or self.data_file
        try:
            self.df = pd.read_csv(fname, parse_dates=['timestamp'])
        except Exception as e:
            logger.warning(f"Failed to load history from {fname}: {e}")
            self.df = pd.DataFrame(columns=['timestamp', 'operation', 'num1', 'num2', 'result'])

    def filter_history(self, **kwargs):
        """Filter history DataFrame by any field (operation, num1, num2, result, etc)."""
        df = self.df
        for key, value in kwargs.items():
            if key in df.columns:
                df = df[df[key] == value]
        return df

    def to_dict(self):
        """Return history as a list of dicts."""
        return self.df.to_dict(orient='records')

    def from_dict(self, dict_list):
        """Load history from a list of dicts."""
        import pandas as pd
        self.df = pd.DataFrame(dict_list)

    def clear_history(self) -> None:
        """Clear the calculation history."""
        self.df = pd.DataFrame(columns=['timestamp', 'operation', 'num1', 'num2', 'result'])
        if os.path.exists(self.data_file):
            try:
                os.remove(self.data_file)
                logger.info(f"Removed history file: {self.data_file}")
            except Exception as e:
                logger.error(f"Error removing history file: {e}")
        logger.info("Cleared calculation history")
    
    def filter_by_operation(self, operation: str) -> List[Calculation]:
        """
        Filter history by operation type.
        
        Args:
            operation (str): Operation to filter by
            
        Returns:
            List[Calculation]: Filtered calculations
        """
        if self.df.empty:
            return []
        
        filtered_df = self.df[self.df['operation'] == operation]
        
        # Convert filtered dataframe rows to Calculation objects
        calculations = []
        for _, row in filtered_df.iterrows():
            calc = Calculation(
                operation=row['operation'],
                num1=row['num1'],
                num2=row['num2'],
                result=row['result']
            )
            calculations.append(calc)
        
        logger.info(f"Filtered history by operation '{operation}': {len(calculations)} results")
        return calculations
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Calculate statistics from history data.
        
        Returns:
            Dict[str, Any]: Dictionary of statistics
        """
        if self.df.empty:
            logger.warning("Cannot calculate statistics: No history data")
            return {}
        
        stats = {}
        
        # Count operations by type
        op_counts = self.df['operation'].value_counts().to_dict()
        stats['operation_counts'] = op_counts
        
        # Calculate average result
        stats['avg_result'] = self.df['result'].mean()
        
        # Get min and max results
        stats['min_result'] = self.df['result'].min()
        stats['max_result'] = self.df['result'].max()
        
        # Count total calculations
        stats['total_calculations'] = len(self.df)
        
        logger.info(f"Generated statistics from {len(self.df)} history records")
        return stats
    
    def get_history(self):
        """Return history as list of Calculation objects."""
        return [
            Calculation(
                row['operation'],
                row['num1'],
                row['num2'],
                row['result']
            )
            for _, row in self.df.iterrows()
        ]
    
    def _save_to_csv(self) -> None:
        """Save the current dataframe to CSV file."""
        try:
            self._ensure_data_dir()
            self.df.to_csv(self.data_file, index=False)
            logger.debug(f"Saved history to CSV: {self.data_file}")
        except Exception as e:
            logger.error(f"Error saving history to CSV: {e}")


# Singleton instance
history_manager = HistoryDataManager()
