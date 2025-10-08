
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select reason
from "warehouse"."main_silver"."returns_silver"
where reason is null



  
  
      
    ) dbt_internal_test