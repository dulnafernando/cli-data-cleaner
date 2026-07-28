"""
Data quality profiling functions for the CLI Data Cleaner tool.
"""
import pandas as pd


def count_missing_values(df: pd.DataFrame) -> pd.Series:
    """
    Count missing values in each column of a DataFrame.

    Args:
        df: The DataFrame to analyze.

    Returns:
        A pandas Series mapping column name to count of missing values.
    """
    return df.isna().sum()

def count_duplicate_rows(df: pd.DataFrame) -> int:
    """
    Count the number of duplicate rows in a DataFrame.

    Args:
        df: The DataFrame to analyze.

    Returns:
        The number of rows that are duplicates of an earlier row.
    """
    return int(df.duplicated().sum())