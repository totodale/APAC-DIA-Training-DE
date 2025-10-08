<<<<<<< HEAD
{{ config(materialized='table') }}

with src as (
  select * from {{ ref('_sources') }}
),
typed as (
  select
    cast(supplier_id as bigint) as supplier_id,
    cast(supplier_code as bigint) as supplier_code,
    trim(name) as name,
    trim(country_code) as country_code,
    cast(lead_time_days as bigint) as lead_time_days,
    cast(preferred as boolean) as preferred,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts
  from src
)
select * from typed
=======
{{ config(materialized='table') }}

with src as (
  select * from bronze_suppliers_parquet
),
typed as (
  select
    cast(supplier_id as bigint) as supplier_id,
    supplier_code,
    trim(name) as name,
    country_code,
    cast(lead_time_days as bigint) as lead_time_days,
    cast(preferred as boolean) as preferred
  from src
)
select * from typed;
>>>>>>> 6b0a7aa748829353eba87d52a58aa563944b9ed1
