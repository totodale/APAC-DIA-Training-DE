{{
  config(
    materialized='incremental',
    unique_key='order_id',
    on_schema_change='merge'
  )
}}

SELECT 
a.customer_id as customer_id,
b.product_id as product_id,
c.store_id as store_id,
d.supplier_id as supplier_id,
f.return_id as return_id,
g.date_id as date_id,
e.qty as qty,
e.unit_price as unit_price,
e.line_number as line_total,
e.line_discount_pct as discount_amount,
e.tax_pct as tax_amount,
a.ingestion_ts as ingestion_ts
((e.unit_price +(e.unit_price * e.tax_pct))) - (e.unit_price * e.line_discount_pct) as net_amount
FROM {{ ref('customers_silver') }} AS a
INNER JOIN  {{ ref('products_silver')}} AS b ON a.customer_id = b.product_id
INNER JOIN  {{ ref('stores_silver')}} AS c ON b.product_id = c.store_id
INNER JOIN  {{ ref('suppliers_silver')}} AS d ON c.store_id = d.supplier_id
INNER JOIN  {{ ref('orders_lines_silver')}} AS e ON e.product_id = b.product_id
INNER JOIN  {{ ref('returns_silver')}} AS f ON f.return_id = e.order_id
INNER JOIN  {{ ref('dim_date')}} as g ON g.date_id = a.customer_id

{% if is_incremental() %}
  WHERE a.ingestion_ts > (SELECT MAX(a.ingestion_ts) FROM {{ this }})
{% endif %}