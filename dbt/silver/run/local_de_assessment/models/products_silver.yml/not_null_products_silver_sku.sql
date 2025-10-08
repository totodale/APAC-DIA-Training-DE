
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select sku
from "warehouse"."main_silver"."products_silver"
where sku is null



  
  
      
    ) dbt_internal_test