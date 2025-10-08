
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select latitude
from "warehouse"."main_silver"."stores_silver"
where latitude is null



  
  
      
    ) dbt_internal_test