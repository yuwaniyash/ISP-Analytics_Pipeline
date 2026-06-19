
  create view "postgres"."public"."stg_customers__dbt_tmp"
    
    
  as (
    SELECT
    customer_id,
    name,
    region,
    plan,
    signup_date,
    CASE
        WHEN is_churned = 1 THEN 'Churned'
        ELSE 'Active'
    END AS customer_status,
    CASE
        WHEN plan = 'Basic_10Mbps' THEN 1
        WHEN plan = 'Standard_25Mbps' THEN 2
        WHEN plan = 'Premium_100Mbps' THEN 3
        WHEN plan = 'Ultra_200Mbps' THEN 4
    END AS plan_tier
FROM customers
  );