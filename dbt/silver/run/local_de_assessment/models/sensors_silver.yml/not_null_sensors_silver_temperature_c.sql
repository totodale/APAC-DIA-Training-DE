
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select temperature_c
from "warehouse"."main_silver"."sensors_silver"
where temperature_c is null



  
  
      
    ) dbt_internal_test