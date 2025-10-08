
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select humidity_pct
from "warehouse"."main_silver"."sensors_silver"
where humidity_pct is null



  
  
      
    ) dbt_internal_test