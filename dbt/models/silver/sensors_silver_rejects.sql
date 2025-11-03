{{ config(
    materialized='table',
    contract={'enforced': true}
)}}
select
    cast(sensor_ts as datetime) as sensor_ts,
    cast(store_id as bigint) as store_id,
    cast(shelf_id as bigint) as shelf_id,
    cast(temperature_c as double) as temperature_c,
    cast(humidity_pct as double) as humidity_pct,
    cast(battery_mv as bigint) as battery_mv,
    'FALSE' as isDeleted,
    {{ normalize_timestamp('ingestion_ts') }} as ingestion_ts,
    trim(src_filename) as src_filename,
    trim(src_hash) as src_hash
from {{ ref('stg_sensors') }}
where temperature_c = 0 or
humidity_pct = 0 or
sensor_ts is null