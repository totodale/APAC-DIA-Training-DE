

WITH silver_suppliers AS (
    SELECT * FROM "warehouse"."main_silver"."suppliers_silver"
),
suppliers_gold as (
    SELECT
    *,
    CASE WHEN lead_time_days < 500 THEN 'Super Supplier' 
         WHEN lead_time_days >= 500 THEN 'Mega Supplier'
    else 'Normal Supplier' END as supplier_tier
    FROM silver_suppliers
)
SELECT * FROM suppliers_gold