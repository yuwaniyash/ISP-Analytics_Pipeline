SELECT
    ROW_NUMBER() OVER (ORDER BY plan_tier) AS plan_id,
    plan AS plan_name,
    plan_tier,
    CASE
        WHEN plan = 'Basic_10Mbps' THEN 10
        WHEN plan = 'Standard_25Mbps' THEN 25
        WHEN plan = 'Premium_100Mbps' THEN 100
        WHEN plan = 'Ultra_200Mbps' THEN 200
    END AS speed_mbps,
    CASE
        WHEN plan = 'Basic_10Mbps' THEN 50
        WHEN plan = 'Standard_25Mbps' THEN 100
        WHEN plan = 'Premium_100Mbps' THEN 300
        WHEN plan = 'Ultra_200Mbps' THEN 500
    END AS data_limit_gb,
    CASE
        WHEN plan = 'Basic_10Mbps' THEN 999
        WHEN plan = 'Standard_25Mbps' THEN 1999
        WHEN plan = 'Premium_100Mbps' THEN 3999
        WHEN plan = 'Ultra_200Mbps' THEN 5999
    END AS monthly_price_lkr
FROM (
    SELECT DISTINCT plan, plan_tier FROM "postgres"."public"."stg_customers"
) plans
ORDER BY plan_tier