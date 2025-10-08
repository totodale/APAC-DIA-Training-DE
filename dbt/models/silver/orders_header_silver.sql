{{ config(
    materialized='table',
    contract={'enforced': true}
)}}
select
    cast(order_id as bigint) as order_id,
    cast(order_ts as datetime) as order_ts,
    cast(order_dt_local as date) as date,
    cast(customer_id as bigint) as customer_id,
    cast(channel as bigint) as channel,
    trim(payment_method) as payment_method,
    trim(coupon_code) as coupon_code,
    cast(shipping_fee as bigint) as channel,
    trim(currency) as currency,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts
from {{ source('main','orders_header') }}