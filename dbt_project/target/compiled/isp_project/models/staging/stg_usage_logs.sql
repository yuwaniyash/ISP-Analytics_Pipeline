SELECT
    log_id,
    customer_id,
    date,
    gb_used,
    plan_limit_gb,
    exceeded_limit,
    ROUND(CAST(gb_used * 100.0 / plan_limit_gb AS numeric), 2) AS usage_pct,
    CASE
        WHEN gb_used * 100.0 / plan_limit_gb >= 90 THEN 'High'
        WHEN gb_used * 100.0 / plan_limit_gb >= 50 THEN 'Medium'
        ELSE 'Low'
    END AS usage_category
FROM usage_logs