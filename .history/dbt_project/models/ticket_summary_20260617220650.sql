SELECT
    category,
    status,
    COUNT(*) AS total_tickets,
    SUM(sla_breached) AS breached_count,
    ROUND(SUM(sla_breached) * 100.0 / COUNT(*), 2) AS breach_rate_pct
FROM tickets
GROUP BY category, status