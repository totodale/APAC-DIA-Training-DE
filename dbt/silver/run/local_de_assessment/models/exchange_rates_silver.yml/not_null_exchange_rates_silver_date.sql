
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select date
from "warehouse"."main_silver"."exchange_rates_silver"
where date is null



  
  
      
    ) dbt_internal_test