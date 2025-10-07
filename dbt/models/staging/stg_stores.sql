{{ config(materialized='table') }}

with src as (
  select * from bronze_stores_parquet
),
typed as (
  select
    cast(store_id as bigint) as store_id,
    store_code,
    trim(name) as name,
    cast(channel as bigint) as channel,
    region,
    state,
    cast(latitude as double) as latitude,
    cast(longitude as double) as longitude,
    cast(open_dt as date) as open_dt,
    cast(close_dt as date) as close_dt
  from src
)
select * from typed;
