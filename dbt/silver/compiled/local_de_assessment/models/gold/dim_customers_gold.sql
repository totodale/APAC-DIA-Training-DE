

WITH silver_customers AS (
    SELECT * FROM "warehouse"."main_silver"."customers_silver"
),
customers_enhanced as (
        SELECT
        customer_id,
        natural_key,
        first_name,
        last_name,
        full_name,
        CASE 
            WHEN gdpr_consent = false THEN 'MASKED'
            ELSE email
        END AS email,
        CASE 
            WHEN gdpr_consent = false THEN 'MASKED'
            ELSE phone
        END AS phone,
        address_line1,
        address_line2,
        city,
        state_region
        postcode,
        country_code,
        latitude,
        longitude,
        is_vip,
        join_ts,
        gdpr_consent,
        EXTRACT(YEAR FROM AGE(CURRENT_DATE, birth_date)) AS customer_age,
        join_ts - birth_date as customer_lifetime_days,
        CASE    
            WHEN is_vip = TRUE THEN 'VIP Member'
            WHEN is_vip = FALSE THEN 'Regular Member'
        ELSE 'undefined'
        END as customer_segment,
        ingestion_ts
    FROM silver_customers
)
SELECT * FROM customers_enhanced