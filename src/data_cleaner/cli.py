"""
Command-line interface for the CLI Data Cleaner tool.
"""
import argparse
import sys

from src.data_cleaner.cleaner import (
    load_csv,
    remove_duplicate_rows,
    handle_missing_values,
    standardize_text_columns,
    parse_dates,
)
from src.data_cleaner.profiler import generate_report


def run_pipeline(input_path: str, output_path: str, text_columns: list[str]) -> None:
    """
    Run the full clean-and-profile pipeline on a CSV file.

    Args:
        input_path: Path to the messy input CSV.
        output_path: Path to write the cleaned CSV.
        text_columns: List of text column names to standardize.
    """
    print(f"Loading {input_path}...")
    df = load_csv(input_path)

    print("\n--- Data Quality Report (before cleaning) ---")
    report = generate_report(df)
    print(f"Duplicate rows: {report['duplicate_rows']}")
    print(f"Missing values per column:\n{report['missing_values']}")
    print(f"Outliers found in columns: {list(report['outliers'].keys())}")

    print("\nCleaning data...")
    df = remove_duplicate_rows(df)
    df = handle_missing_values(df, strategy="drop")
    df = parse_dates(df, column="order_date")

    existing_text_columns = [col for col in text_columns if col in df.columns]
    if existing_text_columns:
        df = standardize_text_columns(df, columns=existing_text_columns)

    if "email" in df.columns:
        df["email"] = df["email"].str.strip().str.lower()

    df.to_csv(output_path, index=False)
    print(f"\nCleaned data saved to {output_path}")
    print(f"Rows remaining: {len(df)}")


def main():
    parser = argparse.ArgumentParser(
        description="Clean and profile a messy CSV file."
    )
    parser.add_argument("input_file", help="Path to the messy input CSV file")
    parser.add_argument(
        "--output", default="cleaned_output.csv",
        help="Path to save the cleaned CSV (default: cleaned_output.csv)"
    )
    parser.add_argument(
        "--text-columns", nargs="*", default=[],
        help="Column names to standardize (trim whitespace, title case)"
    )
    args = parser.parse_args()

    try:
        run_pipeline(args.input_file, args.output, args.text_columns)
    except FileNotFoundError:
        print(f"Error: file '{args.input_file}' not found.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()