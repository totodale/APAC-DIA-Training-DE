
  
    
    

    create  table
      "warehouse"."main_stg"."stg_products__dbt_tmp"
  
    as (
      

with src as (
  select * from bronze_products_parquet
),
typed as (
  select
    cast(product_id as bigint) as product_id,
    sku,
    trim(name) as name,
    trim(category) as category,
    subcategory,
    cast(current_price as double) as current_price,
    currency,
    cast(is_discontinued as boolean) as is_discontinued,
    cast(introduced_dt as date) as introducted_dt,
    cast(discontinued_dt as date) as discontinued_dt
  from src
)
select * from typed;
    );
  
  