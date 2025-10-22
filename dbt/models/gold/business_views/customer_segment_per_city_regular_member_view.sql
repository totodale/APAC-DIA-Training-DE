{{
    config(materialized='view')
}}
select 
count(*) as count_customer_segment_per_city,
customer_segment,
city
from {{ ref('dim_customers_gold') }} 
where customer_segment = 'Regular Member'
group by customer_segment, city
order by count_customer_segment_per_city desc