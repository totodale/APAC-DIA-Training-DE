{{
    config(materialized='view')
}}
select 
    count(is_discontinued) total_count,
    is_discontinued
   -- SUM(CASE WHEN is_discontinued = TRUE THEN 1 ELSE 0 END) AS discontinued_product_count,
   --SUM(CASE WHEN is_discontinued = FALSE THEN 1 ELSE 0 END) AS on_going_product_count
from {{ ref('dim_product_scd_gold') }} 
group by is_discontinued
