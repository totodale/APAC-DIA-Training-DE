
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select is_vip
from "warehouse"."main_silver"."customers_silver"
where is_vip is null



  
  
      
    ) dbt_internal_test