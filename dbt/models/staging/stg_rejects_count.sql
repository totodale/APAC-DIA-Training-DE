{% set lake_root = '../lake/_rejects' %}
 
{{ config(
    materialized = 'table'
) }}
select
*
from read_parquet('{{ lake_root }}/parquet/rejects_count/*.parquet')
 