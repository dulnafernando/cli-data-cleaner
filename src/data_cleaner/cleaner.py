"""
Core data cleaning functions for the CLI Data Cleaner tool.
"""
import pandas as pd


def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame and strip whitespace from column names.

    Args:
        file_path: Path to the CSV file to load.

    Returns:
        A pandas DataFrame with cleaned column names.
    """
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    return df
"""
Core data cleaning functions for the CLI Data Cleaner tool.
"""
import pandas as pd


def load_csv(file_path: str) -> pd.DataFrame:
    """
    Load a CSV file into a DataFrame and strip whitespace from column names.

    Args:
        file_path: Path to the CSV file to load.

    Returns:
        A pandas DataFrame with cleaned column names.
    """
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.strip()
    return df


def remove_duplicate_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove exact duplicate rows from a DataFrame.

    Args:
        df: The DataFrame to clean.

    Returns:
        A DataFrame with duplicate rows removed, index reset.
    """
    return df.drop_duplicates().reset_index(drop=True)