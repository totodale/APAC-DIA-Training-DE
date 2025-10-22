{{
    config(materialized='view')
}}
select 
count(currency) as count_of_currency,
currency
from {{ ref('dim_product_scd_gold') }} 
group by currency
order by currency