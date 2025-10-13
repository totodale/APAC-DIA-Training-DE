{% set lake_root = '../lake/bronze' %}
 
{{ config(
    materialized = 'table'
) }}
select
*
from read_parquet('{{ lake_root }}/parquet/orders_lines/*.parquet')
 