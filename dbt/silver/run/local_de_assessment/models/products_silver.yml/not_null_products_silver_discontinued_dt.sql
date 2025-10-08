
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select discontinued_dt
from "warehouse"."main_silver"."products_silver"
where discontinued_dt is null



  
  
      
    ) dbt_internal_test