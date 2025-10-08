
  
  create view "warehouse"."main_stg"."_sources__dbt_tmp" as (
    -- External views pointing at Bronze Parquet/Delta. Adjust path if needed.

 

 
select *
from read_parquet('../lake/bronze/parquet/customers/*.parquet')

--create or replace view bronze_customers_delta as
--select * from delta_scan('../lake/bronze/delta/customers');

--create or replace view bronze_products_parquet as
select * from read_parquet('../lake/bronze/parquet/products/*.parquet');

--create or replace view bronze_products_delta as
--select * from delta_scan('../lake/bronze/delta/products');

--create or replace view bronze_stores_parquet as
select * from read_parquet('../lake/bronze/parquet/stores/*.parquet');

--create or replace view bronze_stores_delta as
select * from delta_scan('../lake/bronze/delta/stores');

--create or replace view bronze_suppliers_parquet as
select * from read_parquet('../lake/bronze/parquet/suppliers/*.parquet');

--create or replace view bronze_suppliers_delta as
select * from delta_scan('../lake/bronze/delta/suppliers');

--create or replace view bronze_orders_header_parquet as
select * from read_parquet('../lake/bronze/parquet/orders_header/*.parquet');

--create or replace view bronze_orders_header_delta as
select * from delta_scan('../lake/bronze/delta/orders_header');

--create or replace view bronze_orders_lines_parquet as
select * from read_parquet('../lake/bronze/parquet/orders_lines/*.parquet');

--create or replace view bronze_orders_lines_delta as
select * from delta_scan('../lake/bronze/delta/orders_lines');

--create or replace view bronze_sensors_parquet as
select * from read_parquet('../lake/bronze/parquet/sensors/*.parquet');

--create or replace view bronze_sensors_delta as
select * from delta_scan('../lake/bronze/delta/sensors');

--create or replace view bronze_exchange_rates_parquet as
select * from read_parquet('../lake/bronze/parquet/exchange_rates/*.parquet');

--create or replace view bronze_exchange_rates_delta as
select * from delta_scan('../lake/bronze/delta/exchange_rates');
  );
