{{
    config(materialized='view')
}}
select 
count(preferred) as count_of_preferred,
preferred,
name
from {{ ref('dim_supplier_gold') }} 
group by preferred,name
order by count_of_preferred desc