"""
data_ingestion.py
-----------------
Day 1, Task 3: Load every provided CSV dataset with Pandas, then print
.shape, .dtypes and .head() for each so we can spot anomalies early.

Put the 10 CSV files the company gave you inside:  data/raw/
Then run from the project root:
    python scripts/data_ingestion.py
"""

from pathlib import Path
import pandas as pd

# ---------------------------------------------------------------------------
# Locate the raw-data folder relative to this script (no hard-coded paths).
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def load_and_inspect(csv_path: Path) -> pd.DataFrame | None:
    """Load one CSV and print a quick inspection summary."""
    print("\n" + "=" * 70)
    print(f"FILE: {csv_path.name}")
    print("=" * 70)

    try:
        df = pd.read_csv(csv_path)
    except Exception as err:
        print(f"  Could not read this file: {err}")
        return None

    # .shape -> (rows, columns)
    print(f"Shape (rows, cols): {df.shape}")

    # .dtypes -> the data type of each column
    print("\nColumn types:")
    print(df.dtypes)

    # .head() -> first 5 rows so we can eyeball the data
    print("\nFirst 5 rows:")
    print(df.head())

    # A quick anomaly check: how many missing values per column?
    missing = df.isnull().sum()
    missing = missing[missing > 0]
    if not missing.empty:
        print("\nNOTE - columns with missing values:")
        print(missing)
    else:
        print("\nNo missing values detected.")

    return df


def main() -> None:
    if not RAW_DIR.exists():
        print(f"Folder not found: {RAW_DIR}")
        print("Create it and place the provided CSV files inside, then re-run.")
        return

    csv_files = sorted(RAW_DIR.glob("*.csv"))

    if not csv_files:
        print(f"No CSV files found in {RAW_DIR}")
        print("Place the 10 provided datasets there and re-run.")
        return

    print(f"Found {len(csv_files)} CSV file(s) in {RAW_DIR.relative_to(PROJECT_ROOT)}")

    loaded = {}
    for csv_path in csv_files:
        df = load_and_inspect(csv_path)
        if df is not None:
            loaded[csv_path.stem] = df

    print("\n" + "=" * 70)
    print(f"DONE — successfully loaded {len(loaded)} of {len(csv_files)} files.")
    print("=" * 70)


if __name__ == "__main__":
    main()
