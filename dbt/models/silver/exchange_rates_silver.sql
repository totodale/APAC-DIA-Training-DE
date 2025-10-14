{{ config(
    materialized='table',
    contract={'enforced': true}
)}}
select
    cast(date as datetime) as date,
    trim(currency) as currency,
    cast(rate_to_aud as double) as rate_to_aud,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts,
    trim(src_filename) as src_filename,
    trim(src_hash) as src_hash
from {{ ref('stg_exchange_rates') }}