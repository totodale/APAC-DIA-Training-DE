{{ config(
    materialized='table',
    contract={'enforced': true}
)}}
select
    trim(event_id) as event_id,
    cast(event_ts as datetime) as event_ts,
    trim(event_type) as event_type,
    trim(user_id) as user_id,
    trim(session_id) as session_id,
    trim(payload.item_sku) as item_sku,
    cast(payload.quantity as bigint) as quantity,
    cast(payload.price as double) as price,
    trim(payload.user_settings_version) as user_settings_version,
    cast(payload.is_mobile as string) as is_mobile,
    {{ normalize_timestamp('ingestion_ts') }} as ingestion_ts,
    trim(src_filename) as src_filename,
    trim(src_hash) as src_hash
from {{ ref('stg_events') }}