
  
    
    

    create  table
      "warehouse"."main"."dim_returns_gold__dbt_tmp"
  
    as (
      
WITH silver_returns AS (
    SELECT * FROM "warehouse"."main_silver"."returns_silver"
),
returns_gold as (
    SELECT
    *
    FROM silver_returns
)
SELECT * FROM returns_gold
    );
  
  