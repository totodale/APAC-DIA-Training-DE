
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select gdpr_consent
from "warehouse"."main_silver"."customers_silver"
where gdpr_consent is null



  
  
      
    ) dbt_internal_test