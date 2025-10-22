{{
    config(materialized='view')
}}
select 
count(supplier_tier) as count_of_supplier_tier,
supplier_tier
from {{ ref('dim_supplier_gold') }} 
group by supplier_tier
order by count_of_supplier_tier desc