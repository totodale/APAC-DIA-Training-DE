
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
((e.unit_price +(e.unit_price * e.tax_pct))) - (e.unit_price * e.line_discount_pct) as net_amount
FROM "warehouse"."main_silver"."customers_silver" AS a
INNER JOIN  "warehouse"."main_silver"."products_silver" AS b ON a.customer_id = b.product_id
INNER JOIN  "warehouse"."main_silver"."stores_silver" AS c ON b.product_id = c.store_id
INNER JOIN  "warehouse"."main_silver"."suppliers_silver" AS d ON c.store_id = d.supplier_id
INNER JOIN  "warehouse"."main_silver"."orders_lines_silver" AS e ON e.product_id = b.product_id
INNER JOIN  "warehouse"."main_silver"."returns_silver" AS f ON f.return_id = e.order_id
INNER JOIN  "warehouse"."main"."dim_date" as g ON g.date_id = a.customer_id