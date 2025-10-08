
  
    
    
      
    

    create  table
      "warehouse"."main_silver"."stores_silver__dbt_tmp"
  
  (
    store_id bigint not null,
    store_code TEXT not null,
    name TEXT not null,
    channel bigint not null,
    region TEXT not null,
    state TEXT not null,
    latitude double not null,
    longitude double not null,
    open_dt date not null,
    close_dt date not null,
    isDeleted TEXT not null,
    ingestion_ts timestamp not null
    
    )
 ;
    insert into "warehouse"."main_silver"."stores_silver__dbt_tmp" 
  (
    
      
      store_id ,
    
      
      store_code ,
    
      
      name ,
    
      
      channel ,
    
      
      region ,
    
      
      state ,
    
      
      latitude ,
    
      
      longitude ,
    
      
      open_dt ,
    
      
      close_dt ,
    
      
      isDeleted ,
    
      
      ingestion_ts 
    
  )
 (
      
    select store_id, store_code, name, channel, region, state, latitude, longitude, open_dt, close_dt, isDeleted, ingestion_ts
    from (
        
select
    cast(store_id as bigint) as store_id,
    trim(store_code) as store_code,
    trim(name) as name,
    cast(channel as bigint) as channel,
    trim(region) as region,
    trim(state) as state,
    cast(latitude as double) as latitude,
    cast(longitude as double) as longitude,
    cast(open_dt as date) as open_dt,
    cast(close_dt as date) as close_dt,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts
from "warehouse"."main"."stores"
    ) as model_subq
    );
  
  