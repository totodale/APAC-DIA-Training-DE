{{
    config(materialized='view')
}}
select 
count(preferred) as count_preferred,
preferred
from {{ ref('dim_supplier_gold') }} 
group by preferred
order by count_preferred desc