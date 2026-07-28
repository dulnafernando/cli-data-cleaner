import pandas as pd
from src.data_cleaner.profiler import count_missing_values


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