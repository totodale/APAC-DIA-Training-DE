
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select delivered_at
from "warehouse"."main_silver"."shipments_silver"
where delivered_at is null



  
  
      
    ) dbt_internal_test