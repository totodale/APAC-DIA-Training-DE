
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select line_discount_pct
from "warehouse"."main_silver"."orders_lines_silver"
where line_discount_pct is null



  
  
      
    ) dbt_internal_test