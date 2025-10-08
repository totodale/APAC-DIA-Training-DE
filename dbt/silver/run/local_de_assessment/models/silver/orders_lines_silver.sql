
  
    
    
      
    

    create  table
      "warehouse"."main_silver"."orders_lines_silver__dbt_tmp"
  
  (
    order_id bigint not null unique,
    line_number bigint not null unique,
    product_id bigint not null unique,
    qty bigint not null,
    unit_price double not null,
    line_discount_pct double not null,
    tax_pct double not null,
    isDeleted varchar not null,
    ingestion_ts timestamp not null
    
    )
 ;
    insert into "warehouse"."main_silver"."orders_lines_silver__dbt_tmp" 
  (
    
      
      order_id ,
    
      
      line_number ,
    
      
      product_id ,
    
      
      qty ,
    
      
      unit_price ,
    
      
      line_discount_pct ,
    
      
      tax_pct ,
    
      
      isDeleted ,
    
      
      ingestion_ts 
    
  )
 (
      
    select order_id, line_number, product_id, qty, unit_price, line_discount_pct, tax_pct, isDeleted, ingestion_ts
    from (
        
select
    cast(order_id as bigint) as order_id,
    cast(line_number as bigint) as line_number,
    cast(product_id as bigint) as product_id,
    cast(qty as bigint) as qty,
    cast(unit_price as double) as unit_price,
    cast(line_discount_pct as double) as line_discount_pct,
    cast(tax_pct as double) as tax_pct,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts
from "warehouse"."main"."orders_lines"
    ) as model_subq
    );
  
  