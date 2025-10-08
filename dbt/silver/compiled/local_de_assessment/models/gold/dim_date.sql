

WITH generate_date AS (
    SELECT 
        CAST(RANGE AS DATE) AS date_key
    FROM 
        RANGE(DATE '2000-01-01', DATE '2030-12-31', INTERVAL 1 DAY)
)
SELECT
    row_number() OVER (Order by date_key) as date_id,
    CAST(strftime(date_key, '%Y%m%d') AS INTEGER) AS date_int_key, -- Surrogate Key for relationships
    EXTRACT(YEAR from date_key) AS year,
    CAST(YEAR(date_key) || RIGHT('0' || MONTH(date_key), 2) AS INTEGER) AS year_month_key,
    MONTH(date_key) AS month_of_year,
    MONTHNAME(date_key) AS month_name,
    DAYOFMONTH(date_key) AS day_of_month,
    DAYOFYEAR(date_key) AS day_of_year,
    QUARTER(date_key) AS quarter_of_year,
    CAST(YEAR(date_key) || QUARTER(date_key) AS INTEGER) AS quarter_key,
    
    -- Weekday Attributes (ISO standard: Monday=1 to Sunday=7)
    ISODOW(date_key) AS day_of_week_iso,
    DAYNAME(date_key) AS day_name,
    CASE 
        WHEN ISODOW(date_key) IN (6, 7) THEN 'Weekend' 
        ELSE 'Weekday' 
    END AS day_type,

    -- Week Attributes (ISO standard)
    WEEKOFYEAR(date_key) AS week_of_year,
    YEARWEEK(date_key) AS year_week_key,

    -- Boundary Dates
    DATE_TRUNC('month', date_key) AS first_day_of_month,
    LAST_DAY(date_key) AS last_day_of_month,
    DATE_TRUNC('quarter', date_key) AS first_day_of_quarter,
    DATE_TRUNC('year', date_key) AS first_day_of_year,
    DATE_TRUNC('year', date_key) - 1 + INTERVAL 1 YEAR AS last_day_of_year,
    
    -- Flags
    CASE WHEN ISODOW(date_key) = 1 THEN TRUE ELSE FALSE END AS is_first_day_of_week,
    CASE WHEN date_key = LAST_DAY(date_key) THEN TRUE ELSE FALSE END AS is_last_day_of_month,
    CASE WHEN dayofmonth(date_key) = 1 THEN TRUE ELSE FALSE END AS is_first_day_of_month,
    CASE WHEN date_key = (DATE_TRUNC('year', date_key) - 1 + INTERVAL 1 YEAR) THEN TRUE ELSE FALSE END AS is_last_day_of_year,
    CASE WHEN dayofyear(date_key) = 1 THEN TRUE ELSE FALSE END AS is_first_day_of_year
FROM
    generate_date
ORDER BY
    date_key