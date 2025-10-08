{{ config(materialized='table') }}

with src as (
  select * from {{ ref('_sources') }}
),
typed as (
  select
    cast(date as datetime) as date,
    trim(currency) as currency,
    cast(rate_to_aud as double) as rate_to_aud,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts
  from src
)
select * from typed
