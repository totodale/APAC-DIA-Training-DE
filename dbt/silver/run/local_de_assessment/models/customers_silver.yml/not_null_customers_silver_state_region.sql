
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select state_region
from "warehouse"."main_silver"."customers_silver"
where state_region is null



  
  
      
    ) dbt_internal_test