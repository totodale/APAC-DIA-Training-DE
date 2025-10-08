
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select is_discontinued
from "warehouse"."main_silver"."products_silver"
where is_discontinued is null



  
  
      
    ) dbt_internal_test