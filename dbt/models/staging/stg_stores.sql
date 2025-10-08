{{ config(materialized='table') }}

with src as (
  select * from {{ ref('_sources') }}
),
typed as (
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
    cast(ingestion_ts as datetime) as ingestion_ts
  from src
)
select * from typed
