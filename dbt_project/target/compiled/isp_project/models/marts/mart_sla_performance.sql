SELECT
    category,
    region,
    COUNT(*) AS total_tickets,
    SUM(sla_breached) AS breached_count,
    ROUND(SUM(sla_breached) * 100.0 / COUNT(*), 2) AS breach_rate_pct,
    ROUND(AVG(days_to_resolve), 1) AS avg_days_to_resolve
FROM "postgres"."public"."fact_tickets"
GROUP BY category, region
ORDER BY breach_rate_pct DESC