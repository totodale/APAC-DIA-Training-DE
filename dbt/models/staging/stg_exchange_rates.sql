{% set lake_root = '../lake/bronze' %}
 
{{ config(
    materialized = 'table'
) }}
select
*
from read_parquet('{{ lake_root }}/parquet/exchange_rates/*.parquet')
 