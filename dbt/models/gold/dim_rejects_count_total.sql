{{
    config(materialized='table')
}}
select
*
from {{ ref('rejects_count_total_silver') }} 
