{{ config(
    materialized='table',
    contract={'enforced': true}
)}}
select
    cast(order_id as bigint) as order_id,
    cast(order_ts as datetime) as order_ts,
    cast(order_dt_local as date) as date,
    cast(customer_id as bigint) as customer_id,
    trim(channel) as channel,
    trim(payment_method) as payment_method,
    trim(coupon_code) as coupon_code,
    cast(shipping_fee as bigint) as shipping_fee,
    trim(currency) as currency,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts,
    trim(src_filename) as src_filename,
    trim(src_hash) as src_hash
from {{ ref('stg_orders_header') }}
where customer_id != 9999 and
customer_id
in (select customer_id from {{ ref('stg_orders_header') }} 
group by customer_id
having count(customer_id) = 1) and
order_id
in (select order_id from {{ ref('stg_orders_header') }} 
group by order_id
having count(order_id) = 1)