# Data Dictionary — Bluestock Mutual Fund Capstone

This document describes every table and column in `bluestock_mf.db`, their data
types, business meaning, and source file.

---

## dim_fund
*Source: `01_fund_master.csv`* — one row per mutual fund scheme.

| Column | Type | Business definition |
|--------|------|--------------------|
| amfi_code | INTEGER (PK) | Unique AMFI scheme code identifying each fund |
| fund_house | TEXT | Asset Management Company (AMC) that runs the fund |
| scheme_name | TEXT | Full official name of the scheme |
| category | TEXT | Broad asset class (Equity, Debt, etc.) |
| sub_category | TEXT | Specific type (Large Cap, ELSS, Liquid, etc.) |
| launch_date | DATE | Date the scheme was launched |
| risk_category | TEXT | Riskometer grade (Low, Moderate, High, etc.) |

---

## fact_nav
*Source: `02_nav_history.csv` (cleaned)* — daily Net Asset Value per fund.

| Column | Type | Business definition |
|--------|------|--------------------|
| amfi_code | INTEGER (FK → dim_fund) | Fund identifier |
| date | DATE | Calendar date of the NAV (weekends/holidays forward-filled) |
| nav | REAL | Net Asset Value — price per unit on that date (always > 0) |

---

## fact_transactions
*Source: `08_investor_transactions.csv` (cleaned)* — individual investor activity.

| Column | Type | Business definition |
|--------|------|--------------------|
| investor_id | TEXT | Anonymised investor identifier |
| transaction_date | DATE | Date of the transaction |
| amfi_code | INTEGER (FK → dim_fund) | Fund involved |
| transaction_type | TEXT | SIP, Lumpsum, or Redemption (standardised) |
| amount_inr | REAL | Transaction amount in INR (always > 0) |
| state | TEXT | Investor's state |
| city | TEXT | Investor's city |
| city_tier | TEXT | City tier classification (T30 / B30 etc.) |
| age_group | TEXT | Investor age bracket |
| gender | TEXT | Investor gender |
| annual_income_lakh | REAL | Annual income in lakhs INR |
| payment_mode | TEXT | UPI, Cheque, NEFT, etc. |
| kyc_status | TEXT | KYC verification state (Verified / Pending / Rejected) |

---

## fact_performance
*Source: `07_scheme_performance.csv` (cleaned)* — performance metrics per scheme.

| Column | Type | Business definition |
|--------|------|--------------------|
| amfi_code | INTEGER (FK → dim_fund) | Fund identifier |
| scheme_name | TEXT | Scheme name |
| fund_house | TEXT | AMC name |
| category | TEXT | Asset class |
| plan | TEXT | Regular or Direct plan |
| return_1yr_pct | REAL | 1-year return (%) |
| return_3yr_pct | REAL | 3-year annualised return (%) |
| return_5yr_pct | REAL | 5-year annualised return (%) |
| benchmark_3yr_pct | REAL | Benchmark's 3-year return (%) |
| alpha | REAL | Excess return vs benchmark |
| beta | REAL | Volatility relative to market (1 = market) |
| sharpe_ratio | REAL | Return per unit of total risk |
| sortino_ratio | REAL | Return per unit of downside risk |
| std_dev_ann_pct | REAL | Annualised standard deviation (%) |
| max_drawdown_pct | REAL | Largest peak-to-trough drop (%) |
| aum_crore | REAL | Assets under management (₹ crore) |
| expense_ratio_pct | REAL | Annual fee (%), valid range 0.1–2.5 |
| morningstar_rating | INTEGER | 1–5 star rating |
| risk_grade | TEXT | Riskometer grade |

---

## fact_aum
*Source: `03_aum_by_fund_house.csv`* — assets under management by fund house.

| Column | Type | Business definition |
|--------|------|--------------------|
| fund_house | TEXT | AMC name |
| aum_crore | REAL | Total AUM for that fund house (₹ crore) |
| month | TEXT | Reporting month (YYYY-MM) |

---

## dim_date *(optional helper)*
A calendar dimension for time-based analysis.

| Column | Type | Business definition |
|--------|------|--------------------|
| date | DATE (PK) | Calendar date |
| year | INTEGER | Year |
| month | INTEGER | Month number (1–12) |
| month_name | TEXT | Month name |
| quarter | INTEGER | Quarter (1–4) |
| day_of_week | TEXT | Day name |

---

### Notes on cleaning
- **NAV**: forward-filled across weekends/holidays; zero/negative values removed.
- **Transactions**: `transaction_type` standardised to SIP/Lumpsum/Redemption; mixed date formats parsed; negative amounts removed; `kyc_status` standardised.
- **Performance**: all metric columns coerced to numeric; expense-ratio anomalies (outside 0.1–2.5%) flagged.
