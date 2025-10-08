
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select rate_to_aud
from "warehouse"."main_silver"."exchange_rates_silver"
where rate_to_aud is null



  
  
      
    ) dbt_internal_test