
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select full_name
from "warehouse"."main_silver"."customers_silver"
where full_name is null



  
  
      
    ) dbt_internal_test