{{ config(
    materialized='table',
)}}
select
*
from {{ ref('stores_silver_rejects') }}
