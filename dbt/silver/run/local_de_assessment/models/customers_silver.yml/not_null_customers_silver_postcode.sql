
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select postcode
from "warehouse"."main_silver"."customers_silver"
where postcode is null



  
  
      
    ) dbt_internal_test