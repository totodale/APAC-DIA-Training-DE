
  
    
    
      
    

    create  table
      "warehouse"."main_silver"."sensors_silver__dbt_tmp"
  
  (
    sensor_ts timestamp not null,
    store_id bigint not null unique,
    shelf_id bigint not null unique,
    temperature_c double not null,
    humidity_pct double not null,
    battery_mv bigint not null,
    isDeleted TEXT not null,
    ingestion_ts timestamp not null
    
    )
 ;
    insert into "warehouse"."main_silver"."sensors_silver__dbt_tmp" 
  (
    
      
      sensor_ts ,
    
      
      store_id ,
    
      
      shelf_id ,
    
      
      temperature_c ,
    
      
      humidity_pct ,
    
      
      battery_mv ,
    
      
      isDeleted ,
    
      
      ingestion_ts 
    
  )
 (
      
    select sensor_ts, store_id, shelf_id, temperature_c, humidity_pct, battery_mv, isDeleted, ingestion_ts
    from (
        
select
    cast(sensor_ts as datetime) as sensor_ts,
    cast(store_id as bigint) as store_id,
    cast(shelf_id as bigint) as shelf_id,
    cast(temperature_c as double) as temperature_c,
    cast(humidity_pct as double) as humidity_pct,
    cast(battery_mv as bigint) as battery_mv,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts
from "warehouse"."main"."sensors"
    ) as model_subq
    );
  
  