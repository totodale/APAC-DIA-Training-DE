{{ config(
    materialized='table'
)}}
select 
    trim(table_name) as table_name,
    cast(total_reject_count as bigint) as total_reject_count
from {{ ref('stg_rejects_count_total') }} 