
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select coupon_code
from "warehouse"."main_silver"."orders_header_silver"
where coupon_code is null



  
  
      
    ) dbt_internal_test