{{
    config(materialized='view')
}}
select 
count(reason) as return_reason_count,
sum(qty) total_count_of_qty,
reason
from {{ ref('dim_returns_gold') }} 
group by reason
order by return_reason_count desc