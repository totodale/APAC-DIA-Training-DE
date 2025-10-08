
  
    
    
      
    

    create  table
      "warehouse"."main_silver"."shipments_silver__dbt_tmp"
  
  (
    shipment_id bigint not null unique,
    order_id bigint not null unique,
    carrier TEXT not null,
    shipped_at timestamp not null,
    delivered_at timestamp not null,
    ship_cost bigint not null,
    isDeleted TEXT not null,
    ingestion_ts timestamp not null
    
    )
 ;
    insert into "warehouse"."main_silver"."shipments_silver__dbt_tmp" 
  (
    
      
      shipment_id ,
    
      
      order_id ,
    
      
      carrier ,
    
      
      shipped_at ,
    
      
      delivered_at ,
    
      
      ship_cost ,
    
      
      isDeleted ,
    
      
      ingestion_ts 
    
  )
 (
      
    select shipment_id, order_id, carrier, shipped_at, delivered_at, ship_cost, isDeleted, ingestion_ts
    from (
        
select
    cast(shipment_id as bigint) as shipment_id,
    cast(order_id as bigint) as order_id,
    trim(carrier) as carrier,
    cast(shipped_at as datetime) as shipped_at,
    cast(delivered_at as datetime) as delivered_at,
    cast(ship_cost as bigint) as ship_cost,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts
from "warehouse"."main"."shipments"
    ) as model_subq
    );
  
  