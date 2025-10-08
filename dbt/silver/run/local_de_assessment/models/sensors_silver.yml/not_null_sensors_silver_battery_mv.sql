
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select battery_mv
from "warehouse"."main_silver"."sensors_silver"
where battery_mv is null



  
  
      
    ) dbt_internal_test