{{ config(materialized='table') }}

with src as (
  select * from {{ ref('_sources') }}
),
typed as (
  select
    cast(order_id as bigint) as order_id,
    cast(order_ts as datetime) as order_ts,
    cast(order_dt_local as date) as date,
    cast(customer_id as bigint) as customer_id,
    cast(channel as bigint) as channel,
    payment_method,
    coupon_code,
    cast(shipping_fee as bigint) as channel,
    currency
  from src
)
select * from typed

