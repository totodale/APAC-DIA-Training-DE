{{
    config(materialized='view')
}}
select 
count(category) as count_of_product_category,
round(sum(current_price),2) as sum_of_product_category,
category
from {{ ref('dim_product_scd_gold') }} 
group by category
order by count_of_product_category desc, sum_of_product_category desc