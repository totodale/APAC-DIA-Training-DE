
  
    
    

    create  table
      "warehouse"."main_stg"."stg_exchange_rates__dbt_tmp"
  
    as (
      

with src as (
  select * from bronze_exchange_rates_parquet
),
typed as (
  select
    cast(date as datetime) as date,
    currency,
    cast(rate_to_aud as double) as rate_to_aud
  from src
)
select * from typed;
    );
  
  