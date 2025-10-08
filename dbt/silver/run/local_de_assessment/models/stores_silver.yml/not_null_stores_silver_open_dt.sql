
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select open_dt
from "warehouse"."main_silver"."stores_silver"
where open_dt is null



  
  
      
    ) dbt_internal_test