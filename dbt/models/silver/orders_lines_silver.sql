{{ config(
    materialized='table',
    contract={'enforced': true}
)}}
select
    cast(order_id as bigint) as order_id,
    cast(line_number as bigint) as line_number,
    cast(product_id as bigint) as product_id,
    cast(qty as bigint) as qty,
    cast(unit_price as double) as unit_price,
    cast(line_discount_pct as double) as line_discount_pct,
    cast(tax_pct as double) as tax_pct,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts
    trim(src_filename) as src_filename,
    trim(src_hash) as src_hash
from {{ source('main','orders_lines') }}