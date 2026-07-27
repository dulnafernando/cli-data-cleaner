import pandas as pd
from src.data_cleaner.cleaner import load_csv, remove_duplicate_rows


def test_load_csv_strips_column_whitespace(tmp_path):
    # Arrange: create a tiny temp CSV with messy headers
    csv_content = "  name ,age\nAlice,30\nBob,25\n"
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_content)

    # Act
    df = load_csv(str(file_path))

    # Assert
    assert list(df.columns) == ["name", "age"]
    assert len(df) == 2


def test_remove_duplicate_rows(tmp_path):
    # Arrange: Alice appears twice, Bob once
    csv_content = "name,age\nAlice,30\nAlice,30\nBob,25\n"
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_content)
    df = load_csv(str(file_path))

    # Act
    cleaned_df = remove_duplicate_rows(df)

    # Assert
    assert len(cleaned_df) == 2
    assert cleaned_df["name"].tolist() == ["Alice", "Bob"]