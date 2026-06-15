"""
live_nav_fetch.py
-----------------
Day 1, Tasks 4 & 5: Fetch live NAV (Net Asset Value) data for mutual fund
schemes from the public mfapi.in API, then save each as a raw CSV file.

Run from the project root:
    python scripts/live_nav_fetch.py
"""

from pathlib import Path
import requests
import pandas as pd

# ---------------------------------------------------------------------------
# 1. Define where raw files will be saved (NEVER hard-code full paths!)
#    Path(__file__).parent goes up from /scripts to the project root.
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)  # create folder if missing

# ---------------------------------------------------------------------------
# 2. The 6 schemes we need (Task 4 = HDFC Top 100, Task 5 = the other 5)
#    Format: { "Friendly Name": scheme_code }
# ---------------------------------------------------------------------------
SCHEMES = {
    "HDFC_Top_100_Direct": 125497,   # Task 4
    "SBI_Bluechip": 119551,          # Task 5
    "ICICI_Bluechip": 120503,
    "Nippon_Large_Cap": 118632,
    "Axis_Bluechip": 119092,
    "Kotak_Bluechip": 120841,
}

BASE_URL = "https://api.mfapi.in/mf/{code}"


def fetch_one_scheme(name: str, code: int) -> pd.DataFrame | None:
    """Fetch a single scheme's NAV history, return it as a clean DataFrame."""
    url = BASE_URL.format(code=code)
    print(f"Fetching {name} (code {code}) ...")

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()          # raises an error on a bad response
        payload = response.json()            # convert JSON text -> Python dict
    except requests.exceptions.RequestException as err:
        print(f"  -> FAILED for {name}: {err}")
        return None

    # The API returns:  { "meta": {...}, "data": [ {date, nav}, ... ] }
    records = payload.get("data", [])
    if not records:
        print(f"  -> No NAV records returned for {name}")
        return None

    df = pd.DataFrame(records)               # columns: 'date', 'nav'
    # Add identifying columns so we know which scheme each row belongs to
    df["scheme_code"] = code
    df["scheme_name"] = name
    # Fix data types: date as datetime, nav as a number
    df["date"] = pd.to_datetime(df["date"], format="%d-%m-%Y", errors="coerce")
    df["nav"] = pd.to_numeric(df["nav"], errors="coerce")
    df = df.sort_values("date").reset_index(drop=True)

    print(f"  -> OK: {df.shape[0]} rows fetched")
    return df


def main() -> None:
    all_frames = []

    for name, code in SCHEMES.items():
        df = fetch_one_scheme(name, code)
        if df is None:
            continue

        # Save this scheme's raw CSV individually
        out_path = RAW_DIR / f"nav_{name}.csv"
        df.to_csv(out_path, index=False)
        print(f"     saved -> {out_path.relative_to(PROJECT_ROOT)}")

        all_frames.append(df)

    # Also save one combined file with every scheme stacked together
    if all_frames:
        combined = pd.concat(all_frames, ignore_index=True)
        combined_path = RAW_DIR / "nav_all_schemes.csv"
        combined.to_csv(combined_path, index=False)
        print(f"\nCombined file saved -> {combined_path.relative_to(PROJECT_ROOT)}")
        print(f"Total rows across all schemes: {combined.shape[0]}")
    else:
        print("\nNo data was fetched. Check your internet connection.")


if __name__ == "__main__":
    main()
