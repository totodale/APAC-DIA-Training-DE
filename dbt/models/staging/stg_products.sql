{{ config(materialized='table') }}

with src as (
  select * from {{ ref('_sources') }}
),
typed as (
  select
    cast(product_id as bigint) as product_id,
    trim(sku) as sku,
    trim(name) as name,
    trim(category) as category,
    trim(subcategory) as subcategory,
    cast(current_price as double) as current_price,
    trim(currency) as currency,
    cast(is_discontinued as boolean) as is_discontinued,
    cast(introduced_dt as date) as introduced_dt,
    cast(discontinued_dt as date) as discontinued_dt,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts
  from src
)
select * from typed
