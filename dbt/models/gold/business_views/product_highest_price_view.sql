{{
    config(materialized='view')
}}
select 
name,
category,
current_price
from {{ ref('dim_product_scd_gold') }} 
order by current_price desc
