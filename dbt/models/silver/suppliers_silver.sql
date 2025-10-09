{{ config(
    materialized='table',
    contract={'enforced': true}
)}}
select
    cast(supplier_id as bigint) as supplier_id,
    cast(supplier_code as bigint) as supplier_code,
    trim(name) as name,
    trim(country_code) as country_code,
    cast(lead_time_days as bigint) as lead_time_days,
    cast(preferred as boolean) as preferred,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts,
    trim(src_filename) as src_filename,
    trim(src_hash) as src_hash
from {{ source('main','suppliers') }}