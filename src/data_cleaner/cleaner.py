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


def handle_missing_values(df: pd.DataFrame, strategy: str = "drop") -> pd.DataFrame:
    """
    Handle missing values in a DataFrame.

    Args:
        df: The DataFrame to clean.
        strategy: How to handle missing values. One of:
            "drop" - remove any row containing a missing value.
            "fill_mean" - fill missing numeric values with the column mean.

    Returns:
        A DataFrame with missing values handled, index reset.

    Raises:
        ValueError: If an unsupported strategy is given.
    """
    if strategy == "drop":
        return df.dropna().reset_index(drop=True)
    elif strategy == "fill_mean":
        return df.fillna(df.mean(numeric_only=True)).reset_index(drop=True)
    else:
        raise ValueError(f"Unknown strategy: {strategy}")

def standardize_text_columns(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """
    Strip whitespace and apply title case to specified text columns.

    Args:
        df: The DataFrame to clean.
        columns: List of column names to standardize.

    Returns:
        A DataFrame with the specified columns cleaned.
    """
    df = df.copy()
    for col in columns:
        df[col] = df[col].str.strip().str.title()
    return df