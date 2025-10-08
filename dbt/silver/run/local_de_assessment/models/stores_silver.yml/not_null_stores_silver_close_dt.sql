
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select close_dt
from "warehouse"."main_silver"."stores_silver"
where close_dt is null



  
  
      
    ) dbt_internal_test