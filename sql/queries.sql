-- ============================================================
-- queries.sql  —  10 analytical queries (Day 2, Task 6)
-- ============================================================

-- Q1. Top 5 funds by AUM
SELECT scheme_name, fund_house, aum_crore
FROM fact_performance
ORDER BY aum_crore DESC
LIMIT 5;

-- Q2. Average NAV per month for each fund
SELECT amfi_code,
       strftime('%Y-%m', date) AS month,
       ROUND(AVG(nav), 4)      AS avg_nav
FROM fact_nav
GROUP BY amfi_code, month
ORDER BY amfi_code, month;

-- Q3. SIP year-over-year growth (total SIP amount per year)
SELECT strftime('%Y', transaction_date) AS year,
       ROUND(SUM(amount_inr), 2)        AS total_sip_inr
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY year
ORDER BY year;

-- Q4. Transactions by state (count and total value)
SELECT state,
       COUNT(*)                  AS num_transactions,
       ROUND(SUM(amount_inr), 2) AS total_value_inr
FROM fact_transactions
GROUP BY state
ORDER BY total_value_inr DESC;

-- Q5. Funds with expense ratio below 1%
SELECT scheme_name, fund_house, expense_ratio_pct
FROM fact_performance
WHERE expense_ratio_pct < 1.0
ORDER BY expense_ratio_pct ASC;

-- Q6. Top 10 funds by 3-year return
SELECT scheme_name, fund_house, return_3yr_pct
FROM fact_performance
ORDER BY return_3yr_pct DESC
LIMIT 10;

-- Q7. Number of funds per fund house
SELECT fund_house, COUNT(*) AS num_funds
FROM dim_fund
GROUP BY fund_house
ORDER BY num_funds DESC;

-- Q8. Transaction mix by type (SIP vs Lumpsum vs Redemption)
SELECT transaction_type,
       COUNT(*)                  AS num_transactions,
       ROUND(SUM(amount_inr), 2) AS total_value_inr
FROM fact_transactions
GROUP BY transaction_type
ORDER BY total_value_inr DESC;

-- Q9. Average expense ratio by category
SELECT category,
       ROUND(AVG(expense_ratio_pct), 3) AS avg_expense_ratio
FROM fact_performance
GROUP BY category
ORDER BY avg_expense_ratio;

-- Q10. Best risk-adjusted funds (highest Sharpe ratio)
SELECT scheme_name, fund_house, sharpe_ratio, return_3yr_pct
FROM fact_performance
ORDER BY sharpe_ratio DESC
LIMIT 5;
