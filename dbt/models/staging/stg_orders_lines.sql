{{ config(materialized='table') }}

with src as (
  select * from {{ ref('_sources') }}
),
typed as (
  select
    cast(order_id as bigint) as order_id,
    cast(line_number as bigint) as line_number,
    cast(product_id as bigint) as product_id,
    cast(qty as bigint) as qty,
    cast(unit_price as double) as unit_price,
    cast(line_discount_pct as double) as line_discount_pct,
    cast(tax_pct as double) as tax_pct
  from src
)
select * from typed
