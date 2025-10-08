
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select isDeleted
from "warehouse"."main_silver"."returns_silver"
where isDeleted is null



  
  
      
    ) dbt_internal_test