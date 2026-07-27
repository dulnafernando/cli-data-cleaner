# CLI Data Cleaner & Profiler

A command-line tool for cleaning and profiling messy CSV data — built as Project 1 of a structured Data Engineering portfolio.

## Problem

Raw data from spreadsheets, exports, and legacy systems is rarely clean. It typically contains duplicate rows, missing values, inconsistent formatting (dates, casing, whitespace), and incorrect data types. Before any analysis, ETL pipeline, or machine learning model can run reliably, this data needs to be cleaned. This is one of the most common first tasks a Data Engineer performs in industry.

## What This Project Does

Given a messy CSV file, this tool:
- Loads the data and normalizes column headers
- Removes exact duplicate rows
- Handles missing values (configurable: drop rows or fill with column mean)
- Standardizes text formatting (trims whitespace, normalizes casing)
- Parses inconsistent date formats into a single, consistent format
- *(In progress)* Generates a data quality report summarizing issues found
- *(In progress)* Exposes all of the above through a command-line interface

## Tech Stack

- **Python 3.14**
- **pandas** — data manipulation
- **pytest** — testing framework
- **argparse** *(planned)* — CLI interface

## Project Structure

```
cli-data-cleaner/
├── README.md
├── requirements.txt
├── setup.py
├── pytest.ini
├── .gitignore
├── src/
│   └── data_cleaner/
│       ├── __init__.py
│       ├── cleaner.py       # core data cleaning functions
│       ├── profiler.py      # data quality reporting (in progress)
│       ├── cli.py           # command-line interface (in progress)
│       └── utils.py
├── tests/
│   ├── test_cleaner.py
│   └── test_profiler.py
├── sample_data/
│   └── messy_sales_data.csv
└── docs/
    └── design_notes.md
```

## Core Functions (`cleaner.py`)

| Function | Purpose |
|---|---|
| `load_csv(file_path)` | Loads a CSV and strips whitespace from column headers |
| `remove_duplicate_rows(df)` | Removes exact duplicate rows |
| `handle_missing_values(df, strategy)` | Drops rows with missing values, or fills numeric columns with the column mean |
| `standardize_text_columns(df, columns)` | Trims whitespace and applies title case to specified text columns |
| `parse_dates(df, column)` | Converts a column of mixed-format date strings into proper datetime objects |

Each function takes a `pandas.DataFrame` in and returns a cleaned `DataFrame` out, without mutating the original — keeping the cleaning pipeline composable and side-effect-free.

## Sample Dataset

`sample_data/messy_sales_data.csv` is a deliberately messy 15-row sales dataset containing:
- Duplicate rows
- Missing values (quantity, price, customer name)
- Inconsistent date formats (`2024-01-15`, `01/16/2024`, `2024/01/19`, `15-01-2024`)
- Inconsistent text casing (`"South"` vs `"south"`)
- Leading/trailing whitespace in names and column headers
- Negative quantities (data entry errors)
- A likely price outlier

This dataset is used both for manual testing and as a realistic target for the cleaning pipeline.

## Getting Started

### Prerequisites
- Python 3.14+
- Git

### Setup

```bash
git clone https://github.com/dulnafernando/cli-data-cleaner.git
cd cli-data-cleaner
python -m venv venv
venv\Scripts\Activate.ps1      # Windows PowerShell
pip install -r requirements.txt
```

### Running Tests

```bash
pytest tests/ -v
```

## Development Approach

This project is built using **Test-Driven Development (TDD)**: for each function, a failing test is written first (red), then the minimum code needed to pass it is implemented (green), before moving to the next function. This ensures every function in `cleaner.py` has test coverage from the moment it's written, and forces a clear definition of expected behavior before implementation.

## Design Decisions

- **Functions return new DataFrames rather than mutating in place** — this avoids surprising side effects when functions are chained together in a pipeline, at a small memory cost that's acceptable for the dataset sizes this tool targets.
- **`handle_missing_values` uses a strategy parameter rather than separate functions** — mirrors the flexible design of pandas' own API (`dropna`/`fillna`) while giving the caller one clear entry point.
- **`parse_dates` uses `format="mixed"`** — real-world data frequently mixes date formats across rows (e.g., manual entry vs. system export); this lets pandas infer each value's format individually rather than assuming a single format for the whole column.

## Roadmap

- [x] `load_csv` — column header cleaning
- [x] `remove_duplicate_rows`
- [x] `handle_missing_values`
- [x] `standardize_text_columns`
- [x] `parse_dates`
- [ ] `profiler.py` — data quality report (missing value counts, duplicate counts, outlier detection)
- [ ] `cli.py` — command-line interface wiring everything together
- [ ] Integration test against the full sample dataset
- [ ] Outlier detection (IQR-based)
- [ ] Config file support for repeatable cleaning rules

## Author

Dulna Fernando — final-year BSc IT undergraduate, Rajarata University of Sri Lanka, building toward a career in Data Engineering.