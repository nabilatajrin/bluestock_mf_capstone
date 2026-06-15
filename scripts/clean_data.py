"""
clean_data.py
-------------
Day 2, Tasks 1-3: Clean the three messy datasets and save tidy versions
into data/processed/.

Run from the project root:
    python scripts/clean_data.py
"""

from pathlib import Path
import pandas as pd
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def clean_nav() -> None:
    """Task 1 — clean nav_history."""
    print("\n--- TASK 1: Cleaning nav_history ---")
    df = pd.read_csv(RAW_DIR / "02_nav_history.csv")
    before = len(df)

    # parse dates
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # drop rows where date failed to parse
    df = df.dropna(subset=["date"])
    # validate NAV > 0  (removes zero / negative)
    df = df[df["nav"] > 0]
    # remove exact duplicates
    df = df.drop_duplicates()
    # sort by fund then date
    df = df.sort_values(["amfi_code", "date"]).reset_index(drop=True)

    # forward-fill NAV across a full daily calendar per fund (holidays/weekends)
    filled = []
    for code, grp in df.groupby("amfi_code"):
        grp = grp.set_index("date").sort_index()
        full = pd.date_range(grp.index.min(), grp.index.max(), freq="D")
        grp = grp.reindex(full)
        grp["amfi_code"] = code
        grp["nav"] = grp["nav"].ffill()
        grp = grp.rename_axis("date").reset_index()
        filled.append(grp)
    df = pd.concat(filled, ignore_index=True)

    out = PROCESSED_DIR / "02_nav_history_clean.csv"
    df.to_csv(out, index=False)
    print(f"rows {before} -> {len(df)} (after fill). saved {out.name}")


def clean_transactions() -> None:
    """Task 2 — clean investor_transactions."""
    print("\n--- TASK 2: Cleaning investor_transactions ---")
    df = pd.read_csv(RAW_DIR / "08_investor_transactions.csv")
    before = len(df)

    # standardise transaction_type to Title case from a known map
    df["transaction_type"] = df["transaction_type"].astype(str).str.strip().str.lower()
    type_map = {"sip": "SIP", "lumpsum": "Lumpsum", "redemption": "Redemption"}
    df["transaction_type"] = df["transaction_type"].map(type_map)

    # fix dates — handle mixed formats (YYYY-MM-DD, DD-MM-YYYY, YYYY/MM/DD)
    raw_dates = df["transaction_date"].astype(str).str.replace("/", "-", regex=False)
    parsed = pd.to_datetime(raw_dates, errors="coerce", format="mixed", dayfirst=False)
    mask = parsed.isna()
    if mask.any():
        parsed.loc[mask] = pd.to_datetime(
            raw_dates[mask], errors="coerce", format="mixed", dayfirst=True
        )
    df["transaction_date"] = parsed
    n_unparsed = int(df["transaction_date"].isna().sum())
    if n_unparsed:
        print(f"  note: {n_unparsed} dates could not be parsed and were dropped")
    df = df.dropna(subset=["transaction_date"])
    # validate amount
    df["amount_inr"] = pd.to_numeric(df["amount_inr"], errors="coerce")
    df = df[df["amount_inr"] > 0]

    # standardise KYC enum
    df["kyc_status"] = df["kyc_status"].astype(str).str.strip().str.title()
    valid_kyc = {"Verified", "Pending", "Rejected"}
    bad_kyc = set(df["kyc_status"].unique()) - valid_kyc
    if bad_kyc:
        print(f"  note: unexpected KYC values seen: {bad_kyc}")

    df = df.drop_duplicates().reset_index(drop=True)

    out = PROCESSED_DIR / "08_investor_transactions_clean.csv"
    df.to_csv(out, index=False)
    print(f"rows {before} -> {len(df)}. saved {out.name}")
    print(f"  transaction types now: {sorted(df['transaction_type'].dropna().unique())}")


def clean_performance() -> None:
    """Task 3 — clean scheme_performance."""
    print("\n--- TASK 3: Cleaning scheme_performance ---")
    df = pd.read_csv(RAW_DIR / "07_scheme_performance.csv")
    before = len(df)

    # force all return / numeric columns to numbers
    num_cols = [
        "return_1yr_pct", "return_3yr_pct", "return_5yr_pct", "benchmark_3yr_pct",
        "alpha", "beta", "sharpe_ratio", "sortino_ratio", "std_dev_ann_pct",
        "max_drawdown_pct", "aum_crore", "expense_ratio_pct",
    ]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # flag expense_ratio anomalies (valid 0.1% - 2.5%)
    er = df["expense_ratio_pct"]
    anomalies = df[(er < 0.1) | (er > 2.5)]
    if not anomalies.empty:
        print(f"  flagged {len(anomalies)} expense_ratio anomalies (outside 0.1-2.5%):")
        print(anomalies[["amfi_code", "expense_ratio_pct"]].to_string(index=False))

    df = df.drop_duplicates().reset_index(drop=True)

    out = PROCESSED_DIR / "07_scheme_performance_clean.csv"
    df.to_csv(out, index=False)
    print(f"rows {before} -> {len(df)}. saved {out.name}")


def passthrough_rest() -> None:
    """Copy the other already-clean CSVs into processed/ so all 10 live together."""
    print("\n--- Copying remaining clean files to processed/ ---")
    handled = {"02_nav_history.csv", "08_investor_transactions.csv", "07_scheme_performance.csv"}
    for csv in sorted(RAW_DIR.glob("*.csv")):
        if csv.name in handled or csv.name.startswith("nav_"):
            continue
        df = pd.read_csv(csv)
        out = PROCESSED_DIR / csv.name.replace(".csv", "_clean.csv")
        df.to_csv(out, index=False)
        print(f"  copied {csv.name} -> {out.name}")


def main() -> None:
    clean_nav()
    clean_transactions()
    clean_performance()
    passthrough_rest()
    print("\nAll cleaning done. Check data/processed/")


if __name__ == "__main__":
    main()
