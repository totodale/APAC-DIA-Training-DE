
  
    
    

    create  table
      "warehouse"."main_silver"."fct_sales_silver"
  
    as (
      

SELECT 
   a.order_id,
   a.line_number,
   a.product_id,
   c.customer_id,
   b.store_id,
   b.shipping_fee,
   a.qty,
   a.unit_price,
   a.line_discount_pct,
   a.tax_pct
FROM "warehouse"."main"."orders_lines" as a 
inner join "warehouse"."main"."orders_header" as b on a.order_id = b.order_id
inner join "warehouse"."main"."customers" as c on c.customer_id = b.customer_id


    );
  
  
  