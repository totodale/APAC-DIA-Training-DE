
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select currency
from "warehouse"."main_silver"."products_silver"
where currency is null



  
  
      
    ) dbt_internal_test