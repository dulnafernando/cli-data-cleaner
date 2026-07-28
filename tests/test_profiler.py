import pandas as pd
from src.data_cleaner.profiler import count_missing_values, count_duplicate_rows, detect_outliers
def test_count_missing_values():
    # Arrange: age has 1 missing value, name has 0
    df = pd.DataFrame({
        "name": ["Alice", "Bob", "Carol"],
        "age": [30, None, 22]
    })

    # Act
    result = count_missing_values(df)

    # Assert
    assert result["name"] == 0
    assert result["age"] == 1
def test_count_duplicate_rows():
    # Arrange: Alice row appears twice
    df = pd.DataFrame({
        "name": ["Alice", "Alice", "Bob"],
        "age": [30, 30, 25]
    })

    # Act
    result = count_duplicate_rows(df)

    # Assert
    assert result == 1

def test_detect_outliers():
    # Arrange: 8999 is a clear outlier among prices around 800-900
    df = pd.DataFrame({
        "price": [899.99, 850.00, 899.99, 8999.99, 875.00]
    })

    # Act
    outlier_indices = detect_outliers(df, column="price")

    # Assert
    assert 3 in outlier_indices
    assert len(outlier_indices) == 1