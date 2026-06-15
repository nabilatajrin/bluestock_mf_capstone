-- ============================================================
-- schema.sql  —  Bluestock Mutual Fund Capstone (Day 2, Task 4)
-- Star schema: dimension tables + fact tables
-- ============================================================

-- ---------- DIMENSION TABLES ----------

-- dim_fund: one row per mutual fund scheme (the fund master)
CREATE TABLE IF NOT EXISTS dim_fund (
    amfi_code        INTEGER PRIMARY KEY,
    fund_house       TEXT    NOT NULL,
    scheme_name      TEXT    NOT NULL,
    category         TEXT,
    sub_category     TEXT,
    launch_date      DATE,
    risk_category    TEXT
);

-- dim_date: one row per calendar date (helps time-based analysis)
CREATE TABLE IF NOT EXISTS dim_date (
    date        DATE PRIMARY KEY,
    year        INTEGER,
    month       INTEGER,
    month_name  TEXT,
    quarter     INTEGER,
    day_of_week TEXT
);

-- ---------- FACT TABLES ----------

-- fact_nav: daily NAV value per fund
CREATE TABLE IF NOT EXISTS fact_nav (
    amfi_code  INTEGER NOT NULL,
    date       DATE    NOT NULL,
    nav        REAL    NOT NULL,
    PRIMARY KEY (amfi_code, date),
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- fact_transactions: individual investor transactions
CREATE TABLE IF NOT EXISTS fact_transactions (
    investor_id        TEXT,
    transaction_date   DATE,
    amfi_code          INTEGER,
    transaction_type   TEXT,       -- SIP / Lumpsum / Redemption
    amount_inr         REAL,
    state              TEXT,
    city               TEXT,
    city_tier          TEXT,
    age_group          TEXT,
    gender             TEXT,
    annual_income_lakh REAL,
    payment_mode       TEXT,
    kyc_status         TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- fact_performance: performance metrics per scheme
CREATE TABLE IF NOT EXISTS fact_performance (
    amfi_code         INTEGER,
    scheme_name       TEXT,
    fund_house        TEXT,
    category          TEXT,
    plan              TEXT,
    return_1yr_pct    REAL,
    return_3yr_pct    REAL,
    return_5yr_pct    REAL,
    benchmark_3yr_pct REAL,
    alpha             REAL,
    beta              REAL,
    sharpe_ratio      REAL,
    sortino_ratio     REAL,
    std_dev_ann_pct   REAL,
    max_drawdown_pct  REAL,
    aum_crore         REAL,
    expense_ratio_pct REAL,
    morningstar_rating INTEGER,
    risk_grade        TEXT,
    FOREIGN KEY (amfi_code) REFERENCES dim_fund(amfi_code)
);

-- fact_aum: assets under management by fund house over time
CREATE TABLE IF NOT EXISTS fact_aum (
    fund_house TEXT,
    aum_crore  REAL,
    month      TEXT
);
