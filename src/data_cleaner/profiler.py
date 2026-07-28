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

def detect_outliers(df: pd.DataFrame, column: str) -> list[int]:
    """
    Detect outliers in a numeric column using the IQR (Interquartile Range) method.

    Args:
        df: The DataFrame to analyze.
        column: The name of the numeric column to check for outliers.

    Returns:
        A list of row indices where the value is considered an outlier.
    """
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outlier_mask = (df[column] < lower_bound) | (df[column] > upper_bound)
    return df[outlier_mask].index.tolist()

def generate_report(df: pd.DataFrame) -> dict:
    """
    Generate a full data quality report for a DataFrame.

    Args:
        df: The DataFrame to analyze.

    Returns:
        A dictionary containing:
            - duplicate_rows: count of duplicate rows
            - missing_values: per-column missing value counts
            - outliers: dict mapping numeric column names to their outlier row indices
    """
    numeric_columns = df.select_dtypes(include="number").columns
    outliers = {
        col: detect_outliers(df, column=col)
        for col in numeric_columns
        if detect_outliers(df, column=col)
    }

    return {
        "duplicate_rows": count_duplicate_rows(df),
        "missing_values": count_missing_values(df),
        "outliers": outliers,
    }