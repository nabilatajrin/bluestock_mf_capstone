"""
explore_validate.py
--------------------
Day 1, Tasks 6 & 7:
  - Explore the fund master (fund houses, categories, sub-categories, risk grades)
  - Validate that every scheme_code in fund_master exists in nav_history
  - Print a short data quality summary

Run from the project root:
    python scripts/explore_validate.py
"""

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def show_unique(df: pd.DataFrame, possible_names: list[str], label: str) -> None:
    """Print unique values for the first column name that exists in df."""
    for col in possible_names:
        if col in df.columns:
            values = df[col].dropna().unique()
            print(f"\n{label} (column '{col}', {len(values)} unique):")
            print(sorted(values.tolist()))
            return
    print(f"\n{label}: no matching column found. Available columns: {list(df.columns)}")


def main() -> None:
    # ------------------------------------------------------------------
    # TASK 6 — Explore fund master
    # ------------------------------------------------------------------
    fm = pd.read_csv(RAW_DIR / "01_fund_master.csv")

    print("=" * 70)
    print("TASK 6 — FUND MASTER EXPLORATION")
    print("=" * 70)
    print(f"Fund master shape: {fm.shape}")
    print(f"Columns: {list(fm.columns)}")

    # Try common column-name variations so this works whatever the file uses
    show_unique(fm, ["fund_house", "amc", "amc_name", "fund_house_name"], "Fund houses")
    show_unique(fm, ["category", "scheme_category", "fund_category"], "Categories")
    show_unique(fm, ["sub_category", "subcategory", "scheme_sub_category"], "Sub-categories")
    show_unique(fm, ["risk_grade", "risk", "risk_level", "riskometer"], "Risk grades")

    # ------------------------------------------------------------------
    # TASK 7 — Validate AMFI codes against nav_history
    # ------------------------------------------------------------------
    nav = pd.read_csv(RAW_DIR / "02_nav_history.csv")

    print("\n" + "=" * 70)
    print("TASK 7 — AMFI CODE VALIDATION & DATA QUALITY SUMMARY")
    print("=" * 70)

    # Find the scheme-code column in each file (names may vary)
    fm_code_col = next((c for c in ["scheme_code", "amfi_code", "code"] if c in fm.columns), None)
    nav_code_col = next((c for c in ["scheme_code", "amfi_code", "code"] if c in nav.columns), None)

    if fm_code_col is None or nav_code_col is None:
        print("Could not find a scheme_code column in one of the files.")
        print(f"  fund_master columns: {list(fm.columns)}")
        print(f"  nav_history columns: {list(nav.columns)}")
        return

    codes_in_master = set(fm[fm_code_col].dropna().unique())
    codes_in_nav = set(nav[nav_code_col].dropna().unique())

    missing = codes_in_master - codes_in_nav      # in master but NO nav data
    extra = codes_in_nav - codes_in_master        # in nav but not in master

    print(f"Unique scheme codes in fund_master: {len(codes_in_master)}")
    print(f"Unique scheme codes in nav_history: {len(codes_in_nav)}")

    print("\n--- DATA QUALITY SUMMARY ---")
    if not missing:
        print("PASS: every fund_master code has matching NAV history.")
    else:
        print(f"WARNING: {len(missing)} fund_master codes have NO NAV data:")
        print(sorted(missing))

    if extra:
        print(f"NOTE: {len(extra)} codes appear in nav_history but not in fund_master:")
        print(sorted(extra))

    # Overall null check across both files
    print(f"\nTotal missing values in fund_master: {int(fm.isnull().sum().sum())}")
    print(f"Total missing values in nav_history: {int(nav.isnull().sum().sum())}")


if __name__ == "__main__":
    main()
