
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select current_price
from "warehouse"."main_silver"."products_silver"
where current_price is null



  
  
      
    ) dbt_internal_test