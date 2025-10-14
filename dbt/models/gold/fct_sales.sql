{{
    config(
        materialized='incremental',
        unique_key='sale_id',
        on_schema_change='merge'
    )
}}

WITH silver_orders AS (
    SELECT * FROM {{ ref('orders_header_silver') }}
    {% if is_incremental() %}
        WHERE ingestion_ts > (SELECT MAX(ingestion_ts) FROM {{ this }})
    {% endif %}
),
silver_order_lines AS (
    SELECT * FROM {{ ref('orders_lines_silver') }}
),
joined_data AS (
    -- Join and transform Silver tables
    SELECT 
        ol.order_id || '-' || ol.line_number AS sale_id,
        o.order_date,
        o.customer_id,
        ol.product_id,
        -- Calculate metrics
        ol.qty * ol.unit_price AS gross_amount,
        -- more calculations
    FROM silver_order_lines ol
    JOIN silver_orders o ON ol.order_id = o.order_id
)
SELECT * FROM joined_data