
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select name
from "warehouse"."main_silver"."stores_silver"
where name is null



  
  
      
    ) dbt_internal_test