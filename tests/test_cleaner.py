from src.data_cleaner.cleaner import load_csv, remove_duplicate_rows, handle_missing_values, standardize_text_columns

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