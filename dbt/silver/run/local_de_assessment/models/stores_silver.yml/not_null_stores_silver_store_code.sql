
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select store_code
from "warehouse"."main_silver"."stores_silver"
where store_code is null



  
  
      
    ) dbt_internal_test