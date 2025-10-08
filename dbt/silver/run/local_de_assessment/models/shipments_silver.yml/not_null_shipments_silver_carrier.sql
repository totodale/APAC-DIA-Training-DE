
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select carrier
from "warehouse"."main_silver"."shipments_silver"
where carrier is null



  
  
      
    ) dbt_internal_test