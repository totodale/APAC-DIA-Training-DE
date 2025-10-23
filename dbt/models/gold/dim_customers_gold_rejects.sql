{{ config(
    materialized='table'
)}}
select
*
from {{ ref('customers_silver_rejects') }}
