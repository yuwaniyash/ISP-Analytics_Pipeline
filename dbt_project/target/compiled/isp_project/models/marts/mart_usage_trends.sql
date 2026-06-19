SELECT
    f.year,
    f.quarter,
    f.month_number,
    f.month_name,
    f.plan_name,
    f.plan_tier,
    COUNT(DISTINCT f.customer_id) AS active_customers,
    ROUND(AVG(f.gb_used)::numeric, 2) AS avg_gb_used,
    ROUND(AVG(f.usage_pct)::numeric, 2) AS avg_usage_pct,
    SUM(f.exceeded_limit) AS total_exceeded_count
FROM "postgres"."public"."fact_usage" f
GROUP BY f.year, f.quarter, f.month_number, f.month_name, f.plan_name, f.plan_tier
ORDER BY f.year, f.month_number, f.plan_tier