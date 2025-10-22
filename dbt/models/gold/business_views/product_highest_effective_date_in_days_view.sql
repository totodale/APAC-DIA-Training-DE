{{
    config(materialized='view')
}}
select 
effective_date_in_days,
name,
category,
current_price
from {{ ref('dim_product_scd_gold') }} 
order by effective_date_in_days desc
