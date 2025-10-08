
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select state
from "warehouse"."main_silver"."stores_silver"
where state is null



  
  
      
    ) dbt_internal_test