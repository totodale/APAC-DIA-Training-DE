
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select lead_time_days
from "warehouse"."main_silver"."suppliers_silver"
where lead_time_days is null



  
  
      
    ) dbt_internal_test