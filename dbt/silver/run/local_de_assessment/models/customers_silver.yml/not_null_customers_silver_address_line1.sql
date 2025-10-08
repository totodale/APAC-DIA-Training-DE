
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select address_line1
from "warehouse"."main_silver"."customers_silver"
where address_line1 is null



  
  
      
    ) dbt_internal_test