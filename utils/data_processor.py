"""
Data processing utilities for Spotify analytics
"""

import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Any


class DataProcessor:
    """Class for processing and cleaning Spotify playlist data"""
    
    def __init__(self, df: pd.DataFrame):
        """
        Initialize DataProcessor with a DataFrame
        
        Args:
            df: Input DataFrame containing playlist data
        """
        self.df = df.copy()
        
    def clean_data(self) -> pd.DataFrame:
        """
        Clean the dataset by handling missing values and duplicates
        
        Returns:
            Cleaned DataFrame
        """
        # Remove duplicate rows
        self.df = self.df.drop_duplicates()
        
        # Handle missing values (customize based on your needs)
        # Example: fill numeric columns with median
        numeric_columns = self.df.select_dtypes(include=[np.number]).columns
        for col in numeric_columns:
            self.df[col].fillna(self.df[col].median(), inplace=True)
            
        return self.df
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """
        Generate summary statistics for the dataset
        
        Returns:
            Dictionary containing summary statistics
        """
        stats = {
            'total_rows': len(self.df),
            'total_columns': len(self.df.columns),
            'missing_values': self.df.isnull().sum().sum(),
            'duplicate_rows': self.df.duplicated().sum(),
            'numeric_columns': list(self.df.select_dtypes(include=[np.number]).columns),
            'categorical_columns': list(self.df.select_dtypes(include=['object']).columns),
        }
        return stats
    
    def filter_by_column(self, column: str, values: List[Any]) -> pd.DataFrame:
        """
        Filter DataFrame by column values
        
        Args:
            column: Column name to filter by
            values: List of values to filter for
            
        Returns:
            Filtered DataFrame
        """
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")
            
        return self.df[self.df[column].isin(values)]
    
    def aggregate_by_column(self, group_by: str, agg_column: str, 
                           agg_func: str = 'mean') -> pd.DataFrame:
        """
        Aggregate data by a grouping column
        
        Args:
            group_by: Column to group by
            agg_column: Column to aggregate
            agg_func: Aggregation function ('mean', 'sum', 'count', etc.)
            
        Returns:
            Aggregated DataFrame
        """
        if group_by not in self.df.columns or agg_column not in self.df.columns:
            raise ValueError("Specified columns not found in DataFrame")
            
        return self.df.groupby(group_by)[agg_column].agg(agg_func).reset_index()
    
    def get_top_n(self, column: str, n: int = 10, ascending: bool = False) -> pd.DataFrame:
        """
        Get top N rows sorted by a specific column
        
        Args:
            column: Column to sort by
            n: Number of rows to return
            ascending: Sort order (False for descending)
            
        Returns:
            Top N rows DataFrame
        """
        if column not in self.df.columns:
            raise ValueError(f"Column '{column}' not found in DataFrame")
            
        return self.df.nlargest(n, column) if not ascending else self.df.nsmallest(n, column)


def load_and_validate_csv(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load and validate a CSV file
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame if successful, None otherwise
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return None


def export_to_csv(df: pd.DataFrame, output_path: str) -> bool:
    """
    Export DataFrame to CSV file
    
    Args:
        df: DataFrame to export
        output_path: Output file path
        
    Returns:
        True if successful, False otherwise
    """
    try:
        df.to_csv(output_path, index=False)
        return True
    except Exception as e:
        print(f"Error exporting to CSV: {e}")
        return False
