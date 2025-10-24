{{ config(
    materialized='table',
    contract={'enforced': true}
)}}
with getUniqueProductID as 
(
select
    cast(order_id as bigint) as order_id,
    cast(line_number as bigint) as line_number,
    cast(product_id as bigint) as product_id,
    cast(qty as bigint) as qty,
    cast(unit_price as double) as unit_price,
    cast(line_discount_pct as double) as line_discount_pct,
    cast(tax_pct as double) as tax_pct,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts,
    trim(src_filename) as src_filename,
    trim(src_hash) as src_hash,
    row_number() over (partition by product_id order by product_id) as row_number_product_id
from {{ ref('stg_orders_lines') }}
)
select * from getUniqueProductID
where unit_price != 0 and
product_id != -9999 and row_number_product_id = 1