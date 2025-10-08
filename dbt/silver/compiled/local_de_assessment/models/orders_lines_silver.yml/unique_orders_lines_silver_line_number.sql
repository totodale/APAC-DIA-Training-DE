
    
    

select
    line_number as unique_field,
    count(*) as n_records

from "warehouse"."main_silver"."orders_lines_silver"
where line_number is not null
group by line_number
having count(*) > 1


