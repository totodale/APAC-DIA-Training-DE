
    
    

select
    return_id as unique_field,
    count(*) as n_records

from "warehouse"."main_silver"."returns_silver"
where return_id is not null
group by return_id
having count(*) > 1


