{{ config(
    materialized='table',
    contract={'enforced': true}
)}}
with getUniqueStoreCode as 
(
select
    cast(store_id as bigint) as store_id,
    trim(store_code) as store_code,
    trim(name) as name,
    cast(channel as bigint) as channel,
    trim(region) as region,
    trim(state) as state,
    cast(latitude as double) as latitude,
    cast(longitude as double) as longitude,
    cast(open_dt as date) as open_dt,
    cast(close_dt as date) as close_dt,
    'FALSE' as isDeleted,
    {{ normalize_timestamp('ingestion_ts') }} as ingestion_ts,
    trim(src_filename) as src_filename,
    trim(src_hash) as src_hash,
    row_number() over(partition by store_code order by store_code) as row_number_store_code
from {{ ref('stg_stores') }}
)
select * from getUniqueStoreCode
where latitude = -9999 or 
longitude = -9999 or
row_number_store_code > 1