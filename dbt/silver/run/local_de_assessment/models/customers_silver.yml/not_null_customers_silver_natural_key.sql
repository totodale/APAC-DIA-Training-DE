
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select natural_key
from "warehouse"."main_silver"."customers_silver"
where natural_key is null



  
  
      
    ) dbt_internal_test