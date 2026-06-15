"""
build_database.py
-----------------
Day 2, Tasks 4 & 5: Create the SQLite database from schema.sql, then load
every cleaned CSV into it and verify row counts.

Run from the project root (after clean_data.py):
    python scripts/build_database.py
"""

from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
DB_DIR = PROJECT_ROOT / "data" / "db"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "bluestock_mf.db"

# Maps each cleaned CSV to its target table name in the database
CSV_TO_TABLE = {
    "01_fund_master_clean.csv": "dim_fund",
    "02_nav_history_clean.csv": "fact_nav",
    "07_scheme_performance_clean.csv": "fact_performance",
    "08_investor_transactions_clean.csv": "fact_transactions",
    "03_aum_by_fund_house_clean.csv": "fact_aum",
}


def main() -> None:
    if DB_PATH.exists():
        DB_PATH.unlink()  # start fresh each run

    engine = create_engine(f"sqlite:///{DB_PATH}")
    print(f"Database created at: {DB_PATH.relative_to(PROJECT_ROOT)}")

    summary = []
    for csv_name, table in CSV_TO_TABLE.items():
        csv_path = PROCESSED_DIR / csv_name
        if not csv_path.exists():
            print(f"  SKIP (not found): {csv_name}")
            continue

        df = pd.read_csv(csv_path)
        df.to_sql(table, engine, if_exists="replace", index=False)

        # verify: count rows actually written to the DB
        with engine.connect() as conn:
            db_count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()

        match = "OK" if db_count == len(df) else "MISMATCH"
        summary.append((table, len(df), db_count, match))
        print(f"  loaded {csv_name} -> {table}: CSV={len(df)} DB={db_count} [{match}]")

    print("\n--- ROW COUNT VERIFICATION ---")
    for table, csv_n, db_n, match in summary:
        print(f"  {table:<20} csv={csv_n:<8} db={db_n:<8} {match}")

    print("\nDatabase build complete.")


if __name__ == "__main__":
    main()
