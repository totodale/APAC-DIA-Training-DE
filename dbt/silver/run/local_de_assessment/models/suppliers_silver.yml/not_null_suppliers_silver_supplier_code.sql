
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select supplier_code
from "warehouse"."main_silver"."suppliers_silver"
where supplier_code is null



  
  
      
    ) dbt_internal_test