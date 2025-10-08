
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select store_id
from "warehouse"."main_silver"."orders_header_silver"
where store_id is null



  
  
      
    ) dbt_internal_test