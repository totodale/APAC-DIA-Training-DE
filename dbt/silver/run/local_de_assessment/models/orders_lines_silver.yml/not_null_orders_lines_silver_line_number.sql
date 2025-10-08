
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select line_number
from "warehouse"."main_silver"."orders_lines_silver"
where line_number is null



  
  
      
    ) dbt_internal_test