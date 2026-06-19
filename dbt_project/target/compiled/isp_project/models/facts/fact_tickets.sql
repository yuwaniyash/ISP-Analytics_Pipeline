SELECT
    t.ticket_id,
    t.customer_id,
    t.customer_name,
    t.region,
    t.category,
    t.status,
    t.created_at,
    d.month_number,
    d.month_name,
    d.quarter,
    d.year,
    t.resolved_at,
    t.days_to_resolve,
    t.sla_breached
FROM "postgres"."public"."stg_tickets" t
LEFT JOIN "postgres"."public"."dim_dates" d ON t.created_at = d.date