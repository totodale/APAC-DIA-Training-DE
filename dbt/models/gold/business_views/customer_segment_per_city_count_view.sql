{{
    config(materialized='view')
}}
select 
count(*) as count_customer_segment,
customer_segment
from {{ ref('dim_customers_gold') }} 
group by customer_segment
order by count_customer_segment desc