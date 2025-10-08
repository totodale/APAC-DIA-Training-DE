
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select return_ts
from "warehouse"."main_silver"."returns_silver"
where return_ts is null



  
  
      
    ) dbt_internal_test