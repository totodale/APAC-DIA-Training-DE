
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select longitude
from "warehouse"."main_silver"."customers_silver"
where longitude is null



  
  
      
    ) dbt_internal_test