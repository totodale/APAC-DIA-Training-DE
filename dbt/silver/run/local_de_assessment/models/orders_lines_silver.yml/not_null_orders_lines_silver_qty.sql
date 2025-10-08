
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select qty
from "warehouse"."main_silver"."orders_lines_silver"
where qty is null



  
  
      
    ) dbt_internal_test