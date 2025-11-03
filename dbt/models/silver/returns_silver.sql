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
    {{ normalize_timestamp('ingestion_ts') }} as ingestion_ts,
    trim(src_filename) as src_filename,
    trim(src_hash) as src_hash
from {{ ref('stg_returns') }}