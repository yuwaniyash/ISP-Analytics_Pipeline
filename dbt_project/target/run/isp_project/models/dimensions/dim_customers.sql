
  
    

  create  table "isp_db"."public"."dim_customers__dbt_tmp"
  
  
    as
  
  (
    SELECT
    customer_id,
    name,
    region,
    plan,
    plan_tier,
    signup_date,
    customer_status,
    CURRENT_DATE - signup_date AS days_as_customer
FROM "isp_db"."public"."stg_customers"
  );
  