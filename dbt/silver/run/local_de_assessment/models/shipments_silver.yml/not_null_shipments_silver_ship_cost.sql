
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select ship_cost
from "warehouse"."main_silver"."shipments_silver"
where ship_cost is null



  
  
      
    ) dbt_internal_test