SELECT
    t.ticket_id,
    t.customer_id,
    c.name AS customer_name,
    c.region,
    t.category,
    t.status,
    t.created_at,
    CASE
        WHEN t.resolved_at = '' THEN NULL
        ELSE CAST(t.resolved_at AS DATE)
    END AS resolved_at,
    CASE
        WHEN t.resolved_at IS NOT NULL
        THEN t.resolved_at - t.created_at
        ELSE NULL
    END AS days_to_resolve,
    t.sla_breached
FROM tickets t
LEFT JOIN customers c ON t.customer_id = c.customer_id