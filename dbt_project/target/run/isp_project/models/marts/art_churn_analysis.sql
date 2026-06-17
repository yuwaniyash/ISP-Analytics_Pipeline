
  
    

  create  table "isp_db"."public"."art_churn_analysis__dbt_tmp"
  
  
    as
  
  (
    SELECT
    c.region,
    c.plan,
    c.plan_tier,
    COUNT(*) AS total_customers,
    SUM(CASE WHEN c.customer_status = 'Churned' THEN 1 ELSE 0 END) AS churned_customers,
    SUM(CASE WHEN c.customer_status = 'Active' THEN 1 ELSE 0 END) AS active_customers,
    ROUND(SUM(CASE WHEN c.customer_status = 'Churned' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS churn_rate_pct
FROM "isp_db"."public"."dim_customers" c
GROUP BY c.region, c.plan, c.plan_tier
ORDER BY churn_rate_pct DESC
  );
  