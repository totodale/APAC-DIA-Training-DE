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
