
SELECT
    date,
    EXTRACT(DAY FROM date) AS day,
    EXTRACT(MONTH FROM date) AS month_number,
    TO_CHAR(date, 'Month') AS month_name,
    EXTRACT(QUARTER FROM date) AS quarter,
    EXTRACT(YEAR FROM date) AS year,
    CASE
        WHEN EXTRACT(ISODOW FROM date) IN (6, 7) THEN TRUE
        ELSE FALSE
    END AS is_weekend,
    TO_CHAR(date, 'Day') AS day_of_week,
    EXTRACT(ISODOW FROM date) AS day_number
FROM (
    SELECT DISTINCT date FROM {{ ref('stg_usage_logs') }}
) dates
ORDER BY date
