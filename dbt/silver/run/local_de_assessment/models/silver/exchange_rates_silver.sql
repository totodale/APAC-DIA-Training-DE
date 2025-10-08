
  
    
    
      
    

    create  table
      "warehouse"."main_silver"."exchange_rates_silver__dbt_tmp"
  
  (
    date timestamp not null,
    currency TEXT not null,
    rate_to_aud double not null,
    isDeleted TEXT not null,
    ingestion_ts timestamp not null
    
    )
 ;
    insert into "warehouse"."main_silver"."exchange_rates_silver__dbt_tmp" 
  (
    
      
      date ,
    
      
      currency ,
    
      
      rate_to_aud ,
    
      
      isDeleted ,
    
      
      ingestion_ts 
    
  )
 (
      
    select date, currency, rate_to_aud, isDeleted, ingestion_ts
    from (
        
select
    cast(date as datetime) as date,
    currency,
    cast(rate_to_aud as double) as rate_to_aud,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts
from "warehouse"."main"."exchange_rates"
    ) as model_subq
    );
  
  