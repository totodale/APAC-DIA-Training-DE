{{
    config(materialized='table')
}}

WITH silver_products AS (
    SELECT * FROM {{ ref('products_silver') }}
),
product_scd as (
    SELECT
    *,
    discontinued_dt - introduced_dt as effective_date_in_days,
    1 as is_current,   
    FROM silver_products
)
SELECT * FROM product_scd