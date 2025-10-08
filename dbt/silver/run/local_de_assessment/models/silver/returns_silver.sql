
  
    
    
      
    

    create  table
      "warehouse"."main_silver"."returns_silver__dbt_tmp"
  
  (
    return_id bigint not null unique,
    order_id bigint not null unique,
    product_id bigint not null unique,
    return_ts timestamp not null,
    qty bigint not null,
    reason TEXT not null,
    isDeleted TEXT not null,
    ingestion_ts timestamp not null
    
    )
 ;
    insert into "warehouse"."main_silver"."returns_silver__dbt_tmp" 
  (
    
      
      return_id ,
    
      
      order_id ,
    
      
      product_id ,
    
      
      return_ts ,
    
      
      qty ,
    
      
      reason ,
    
      
      isDeleted ,
    
      
      ingestion_ts 
    
  )
 (
      
    select return_id, order_id, product_id, return_ts, qty, reason, isDeleted, ingestion_ts
    from (
        
select
    cast(return_id as bigint) as return_id,
    cast(order_id as bigint) as order_id,
    cast(product_id as bigint) as product_id,
    cast(return_ts as datetime) as return_ts,
    cast(qty as bigint) as qty,
    trim(reason) as reason,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts
 from "warehouse"."main"."returns"
    ) as model_subq
    );
  
  