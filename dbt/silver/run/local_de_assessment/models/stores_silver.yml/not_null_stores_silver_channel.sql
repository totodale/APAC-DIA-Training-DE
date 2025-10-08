
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select channel
from "warehouse"."main_silver"."stores_silver"
where channel is null



  
  
      
    ) dbt_internal_test