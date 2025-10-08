
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select sensor_ts
from "warehouse"."main_silver"."sensors_silver"
where sensor_ts is null



  
  
      
    ) dbt_internal_test