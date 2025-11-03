{{ config(
    materialized='table',
    contract={'enforced': true}
)}}
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
    {{ normalize_timestamp('ingestion_ts') }} as ingestion_ts,
    trim(src_filename) as src_filename,
    trim(src_hash) as src_hash
from {{ ref('stg_products') }}
where discontinued_dt is not null and current_price != -9999