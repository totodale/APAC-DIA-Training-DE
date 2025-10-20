{{ config(
    materialized='table'
)}}
select 
    trim(reason) as reason,
    cast(count as bigint) as count,
    trim(table_name) as table_name
from {{ ref('stg_rejects_count') }} 