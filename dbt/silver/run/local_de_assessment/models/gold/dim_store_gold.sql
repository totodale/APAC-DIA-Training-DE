
  
    
    

    create  table
      "warehouse"."main_gold"."dim_store_gold__dbt_tmp"
  
    as (
      

WITH silver_stores AS (
    SELECT * FROM "warehouse"."main_silver"."stores_silver"
),
stores_gold as (
    SELECT
    *,
    close_dt - open_dt as store_age_days,
    CASE WHEN channel >= 8 THEN 'Very Big'
        WHEN channel  <= 7 THEN 'Big'
        WHEN channel >= 3 AND channel <= 6 THEN 'Medium'
        WHEN channel = 2 THEN 'Small'
    ELSE 'Invalid Size' END as store_size_category,
    CASE WHEN close_dt > '2020-12-31 00:00:00' THEN 'Open'
    ELSE 'Closed' END AS operational_status
    FROM silver_stores
)
SELECT * FROM stores_gold
    );
  
  