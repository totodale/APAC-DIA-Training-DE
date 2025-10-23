{{ config(
    materialized='table'
)}}
select
*
from {{ ref('products_silver_rejects') }}
