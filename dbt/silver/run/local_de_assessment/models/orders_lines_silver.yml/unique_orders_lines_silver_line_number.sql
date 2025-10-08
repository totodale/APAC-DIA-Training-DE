
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    

select
    line_number as unique_field,
    count(*) as n_records

from "warehouse"."main_silver"."orders_lines_silver"
where line_number is not null
group by line_number
having count(*) > 1



  
  
      
    ) dbt_internal_test