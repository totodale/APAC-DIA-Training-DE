{{ config(
    materialized='table',
    contract={'enforced': true}
)}}
select
    cast(return_id as bigint) as return_id,
    cast(order_id as bigint) as order_id,
    cast(product_id as bigint) as product_id,
    cast(return_ts as datetime) as return_ts,
    cast(qty as bigint) as qty,
    trim(reason) as reason,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts
 from {{ source('main','returns') }}