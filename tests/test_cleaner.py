import pandas as pd

from src.data_cleaner.cleaner import load_csv, remove_duplicate_rows, handle_missing_values, standardize_text_columns, parse_dates
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

def test_handle_missing_values_drop(tmp_path):
    # Arrange: Bob has no age (missing value)
    csv_content = "name,age\nAlice,30\nBob,\nCarol,22\n"
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_content)
    df = load_csv(str(file_path))

    # Act
    cleaned_df = handle_missing_values(df, strategy="drop")

    # Assert
    assert len(cleaned_df) == 2
    assert "Bob" not in cleaned_df["name"].tolist()

def test_standardize_text_columns(tmp_path):
    # Arrange: messy whitespace and inconsistent casing
    csv_content = "name,region\n  Mike Wilson  ,south\nJane Doe,NORTH\n"
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_content)
    df = load_csv(str(file_path))

    # Act
    cleaned_df = standardize_text_columns(df, columns=["name", "region"])

    # Assert
    assert cleaned_df["name"].tolist() == ["Mike Wilson", "Jane Doe"]
    assert cleaned_df["region"].tolist() == ["South", "North"]

def test_parse_dates(tmp_path):
    # Arrange: three different date formats, all January 2024
    csv_content = "order_id,order_date\n1,2024-01-15\n2,01/16/2024\n3,15-01-2024\n"
    file_path = tmp_path / "test.csv"
    file_path.write_text(csv_content)
    df = load_csv(str(file_path))

    # Act
    cleaned_df = parse_dates(df, column="order_date")

    # Assert
    assert cleaned_df["order_date"].dtype.name.startswith("datetime")
    assert cleaned_df["order_date"].iloc[0] == pd.Timestamp("2024-01-15")
    assert cleaned_df["order_date"].iloc[1] == pd.Timestamp("2024-01-16")