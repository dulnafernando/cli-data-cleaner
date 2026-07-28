import pandas as pd
from src.data_cleaner.profiler import count_missing_values, count_duplicate_rows

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