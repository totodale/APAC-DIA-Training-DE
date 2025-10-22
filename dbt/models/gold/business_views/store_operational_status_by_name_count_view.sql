{{
    config(materialized='view')
}}
select 
count(operational_status) as count_of_operational_status,
operational_status,
name
from {{ ref('dim_store_gold') }} 
group by operational_status,name
order by count_of_operational_status desc