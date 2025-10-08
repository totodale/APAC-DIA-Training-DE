
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select shelf_id
from "warehouse"."main_silver"."sensors_silver"
where shelf_id is null



  
  
      
    ) dbt_internal_test