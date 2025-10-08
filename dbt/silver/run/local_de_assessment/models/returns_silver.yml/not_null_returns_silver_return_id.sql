
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select return_id
from "warehouse"."main_silver"."returns_silver"
where return_id is null



  
  
      
    ) dbt_internal_test