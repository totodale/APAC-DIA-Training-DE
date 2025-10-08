
  
    
    

    create  table
      "warehouse"."main_gold"."dim_store__dbt_tmp"
  
    as (
      

WITH silver_stores AS (
    SELECT * FROM "warehouse"."main_silver"."stores_silver"
),
stores_gold as (
    SELECT
    *,
    close_dt - open_dt as store_age_days,
    FROM silver_stores
)
SELECT * FROM stores_gold
    );
  
  