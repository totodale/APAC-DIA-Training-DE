-- External views pointing at Bronze Parquet/Delta. Adjust path if needed.
{% set lake_root = '../lake/bronze' %}
 
{{ config(materialized='table') }}
 
select * from read_parquet('{{ lake_root }}/parquet/customers/*.parquet')

--create or replace view bronze_customers_delta as
--select * from delta_scan('{{ lake_root }}/delta/customers');

--create or replace view bronze_products_parquet as
select * from read_parquet('{{ lake_root }}/parquet/products/*.parquet')

--create or replace view bronze_products_delta as
--select * from delta_scan('{{ lake_root }}/delta/products');

--create or replace view bronze_stores_parquet as
select * from read_parquet('{{ lake_root }}/parquet/stores/*.parquet')

--create or replace view bronze_stores_delta as
--select * from delta_scan('{{ lake_root }}/delta/stores')

--create or replace view bronze_suppliers_parquet as
select * from read_parquet('{{ lake_root }}/parquet/suppliers/*.parquet')

--create or replace view bronze_suppliers_delta as
--select * from delta_scan('{{ lake_root }}/delta/suppliers')

--create or replace view bronze_orders_header_parquet as
select * from read_parquet('{{ lake_root }}/parquet/orders_header/*.parquet')

--create or replace view bronze_orders_header_delta as
--select * from delta_scan('{{ lake_root }}/delta/orders_header')

--create or replace view bronze_orders_lines_parquet as
select * from read_parquet('{{ lake_root }}/parquet/orders_lines/*.parquet');

--create or replace view bronze_orders_lines_delta as
--select * from delta_scan('{{ lake_root }}/delta/orders_lines')

--create or replace view bronze_sensors_parquet as
select * from read_parquet('{{ lake_root }}/parquet/sensors/*.parquet');

--create or replace view bronze_sensors_delta as
--select * from delta_scan('{{ lake_root }}/delta/sensors');

--create or replace view bronze_exchange_rates_parquet as
select * from read_parquet('{{ lake_root }}/parquet/exchange_rates/*.parquet');

--create or replace view bronze_exchange_rates_delta as
--select * from delta_scan('{{ lake_root }}/delta/exchange_rates');


