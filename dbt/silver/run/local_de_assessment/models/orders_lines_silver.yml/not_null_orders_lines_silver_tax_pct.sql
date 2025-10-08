
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select tax_pct
from "warehouse"."main_silver"."orders_lines_silver"
where tax_pct is null



  
  
      
    ) dbt_internal_test