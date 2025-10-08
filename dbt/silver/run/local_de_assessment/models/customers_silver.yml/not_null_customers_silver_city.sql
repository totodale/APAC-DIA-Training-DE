
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select city
from "warehouse"."main_silver"."customers_silver"
where city is null



  
  
      
    ) dbt_internal_test