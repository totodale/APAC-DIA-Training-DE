
  
    
    
      
    

    create  table
      "warehouse"."main_silver"."suppliers_silver__dbt_tmp"
  
  (
    supplier_id bigint not null,
    supplier_code bigint not null,
    name TEXT not null,
    country_code TEXT not null,
    lead_time_days bigint not null,
    preferred boolean not null,
    isDeleted varchar not null,
    ingestion_ts timestamp not null
    
    )
 ;
    insert into "warehouse"."main_silver"."suppliers_silver__dbt_tmp" 
  (
    
      
      supplier_id ,
    
      
      supplier_code ,
    
      
      name ,
    
      
      country_code ,
    
      
      lead_time_days ,
    
      
      preferred ,
    
      
      isDeleted ,
    
      
      ingestion_ts 
    
  )
 (
      
    select supplier_id, supplier_code, name, country_code, lead_time_days, preferred, isDeleted, ingestion_ts
    from (
        
select
    cast(supplier_id as bigint) as supplier_id,
    cast(supplier_code as bigint) as supplier_code,
    trim(name) as name,
    trim(country_code) as country_code,
    cast(lead_time_days as bigint) as lead_time_days,
    cast(preferred as boolean) as preferred,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts
from "warehouse"."main"."suppliers"
    ) as model_subq
    );
  
  