{{
    config(materialized='view')
}}
select 
store_age_days,
name,
region,
store_size_category,
operational_status
from {{ ref('dim_store_gold') }} 
order by store_age_days desc