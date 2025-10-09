{{ config(
    materialized='table'
)}}
select
    cast(shipment_id as bigint) as shipment_id,
    cast(order_id as bigint) as order_id,
    trim(carrier) as carrier,
    cast(shipped_at as datetime) as shipped_at,
    cast(delivered_at as datetime) as delivered_at,
    cast(ship_cost as bigint) as ship_cost,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts,
    trim(src_filename) as src_filename,
    trim(src_hash) as src_hash
from {{ source('main','shipments') }}