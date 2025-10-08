
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select introduced_dt
from "warehouse"."main_silver"."products_silver"
where introduced_dt is null



  
  
      
    ) dbt_internal_test