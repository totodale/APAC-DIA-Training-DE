{{
    config(materialized='table')
}}
WITH silver_returns AS (
    SELECT * FROM {{ ref('returns_silver') }}
),
returns_gold as (
    SELECT
    *
    FROM silver_returns
)
SELECT * FROM returns_gold
