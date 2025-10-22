{{
    config(materialized='view')
}}
select 
count(store_size_category) as count_of_store_size_category,
store_size_category
from {{ ref('dim_store_gold') }} 
group by store_size_category
order by count_of_store_size_category desc