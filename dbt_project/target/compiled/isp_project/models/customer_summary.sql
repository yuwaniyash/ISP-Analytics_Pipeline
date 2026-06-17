SELECT
    region,
    plan,
    COUNT(*) AS total_customers,
    SUM(is_churned) AS churned_customers,
    ROUND(SUM(is_churned) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY region, plan