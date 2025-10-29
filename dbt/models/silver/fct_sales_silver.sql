{{
  config(
    materialized='incremental',
    unique_key='order_id',
    on_schema_change='merge'
  )
}}
SELECT
a.order_id as order_id,
a.customer_id as customer_id,
a.store_id as store_id,
a.ingestion_ts as ingestion_ts,
b.line_number as line_number,
b.product_id as product_id,
row_number() over(order by a.customer_id) as date_id,
b.qty as qty,
b.unit_price as unit_price,
b.line_discount_pct as line_discount_pct,
b.tax_pct as tax_pct,
(b.unit_price * b.line_discount_pct) as discount_amount,
(b.unit_price * b.tax_pct) as tax_amount,
(b.qty * b.unit_price) as gross_amount_total,
((b.unit_price +(b.unit_price * b.tax_pct)) - (b.unit_price * b.line_discount_pct)) as net_amount_per_product,
((b.unit_price +(b.unit_price * b.tax_pct)) - (b.unit_price * b.line_discount_pct)) * b.qty as net_amount_total
from {{ ref('stg_orders_header') }} as a 
inner join {{ ref('stg_orders_lines') }} as b on a.order_id = b.order_id
inner join {{ ref('stg_customers') }} as c on a.customer_id = c.customer_id
inner join {{ ref('stg_products') }} as d on b.product_id = d.product_id
inner join {{ ref('stg_returns') }} as e on a.order_id = e.order_id
inner join {{ ref('stg_shipments') }} as f on a.order_id = f.order_id
where b.unit_price != 0 and
discount_amount != 0 and 
tax_amount != 0 and 
net_amount_per_product != 0 and
net_amount_total != 0 and
{% if is_incremental() %}
a.ingestion_ts > (SELECT MAX(ingestion_ts) FROM {{ this }})
{% endif %}
