# Bluestock Mutual Fund Analytics — Capstone Project

An end-to-end data analytics pipeline for Indian mutual fund data, built as part of a Data Analyst internship at Bluestock Fintech. The project ingests live and historical mutual fund data, cleans and validates it, loads it into a SQLite database, and produces analytical insights and visualisations.

## Overview

This project analyses **40 mutual fund schemes across 10 fund houses**, covering daily NAV history, investor transactions, scheme performance, AUM, SIP inflows, and portfolio holdings. It follows a structured ETL → database → analysis workflow.

## Tech Stack

- **Python** — pandas, numpy
- **Data fetching** — requests (mfapi.in API)
- **Database** — SQLite via SQLAlchemy
- **Visualisation** — matplotlib, seaborn, plotly
- **Notebooks** — Jupyter

## Project Structure

```
bluestock_mf_capstone/
├── data/
│   ├── raw/            # original downloaded files (gitignored)
│   └── processed/      # cleaned CSVs (gitignored)
├── notebooks/
│   └── EDA_Analysis.ipynb
├── scripts/
│   ├── data_ingestion.py    # load & inspect provided datasets
│   ├── live_nav_fetch.py    # fetch live NAV from mfapi.in
│   ├── clean_data.py        # clean nav, transactions, performance
│   └── build_database.py    # load cleaned data into SQLite
├── sql/
│   ├── schema.sql           # star schema (dim + fact tables)
│   └── queries.sql          # 10 analytical queries
├── data_dictionary.md       # column documentation
└── requirements.txt
```

## What the Pipeline Does

**1. Data Ingestion**
Fetches live NAV history for key schemes (HDFC Top 100, SBI Bluechip, ICICI Bluechip, and others) from the public mfapi.in API, and loads ten provided datasets covering fund master data, transactions, performance, AUM, and holdings.

**2. Data Cleaning**
Parses and standardises dates, forward-fills NAV across weekends and holidays, removes invalid records, standardises transaction types (SIP / Lumpsum / Redemption), and validates value ranges.

**3. Database**
Loads cleaned data into a SQLite star schema with dimension and fact tables (`dim_fund`, `fact_nav`, `fact_transactions`, `fact_performance`, `fact_aum`), verified by row-count checks.

**4. Exploratory Analysis**
A Jupyter notebook produces 15+ charts covering NAV trends, AUM growth, SIP inflows, investor demographics, geographic distribution, folio growth, return correlations, and sector allocation.

## Getting Started

```bash
# Clone the repo
git clone https://github.com/nabilatajrin/bluestock_mf_capstone.git
cd bluestock_mf_capstone

# Install dependencies
pip install -r requirements.txt

# Fetch live NAV data
python scripts/live_nav_fetch.py

# Clean the data
python scripts/clean_data.py

# Build the database
python scripts/build_database.py
```

Then open `notebooks/EDA_Analysis.ipynb` to explore the analysis.

## Key Highlights

- ~64,000 rows of daily NAV data processed across 40 schemes
- 32,000+ investor transactions cleaned and standardised
- 10-table SQLite database with verified data integrity
- 15+ interactive and static visualisations

## Data Source

Live NAV data from [mfapi.in](https://www.mfapi.in/), a free public API for Indian mutual fund data. Supplementary datasets provided as part of the Bluestock Fintech capstone.

## Author

**Nabila Tajrin Bristy**
Data Analyst Intern, Bluestock Fintech
M.Sc. Mathematics & Data Science
