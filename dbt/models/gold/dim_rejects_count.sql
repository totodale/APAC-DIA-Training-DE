{{
    config(materialized='table')
}}
select
*
from {{ ref('rejects_count_silver') }} 
order by table_name, count desc