
  create view "isp_db"."public"."daily_usage__dbt_tmp"
    
    
  as (
    SELECT
    customer_id,
    date,
    gb_used,
    plan_limit_gb,
    exceeded_limit,
    ROUND(gb_used * 100.0 / plan_limit_gb, 2) AS usage_pct
FROM usage_logs
  );