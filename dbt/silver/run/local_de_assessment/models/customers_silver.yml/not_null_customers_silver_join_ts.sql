
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select join_ts
from "warehouse"."main_silver"."customers_silver"
where join_ts is null



  
  
      
    ) dbt_internal_test