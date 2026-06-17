
  
    

  create  table "isp_db"."public"."fact_usage__dbt_tmp"
  
  
    as
  
  (
    SELECT
    u.log_id,
    u.customer_id,
    u.date,
    d.month_number,
    d.month_name,
    d.quarter,
    d.year,
    d.is_weekend,
    p.plan_name,
    p.plan_tier,
    p.speed_mbps,
    u.gb_used,
    u.plan_limit_gb,
    u.usage_pct,
    u.usage_category,
    u.exceeded_limit
FROM "isp_db"."public"."stg_usage_logs" u
LEFT JOIN "isp_db"."public"."dim_dates" d ON u.date = d.date
LEFT JOIN "isp_db"."public"."dim_plans" p ON u.customer_id = (
    SELECT customer_id FROM "isp_db"."public"."dim_customers"
    WHERE customer_id = u.customer_id LIMIT 1
)
  );
  