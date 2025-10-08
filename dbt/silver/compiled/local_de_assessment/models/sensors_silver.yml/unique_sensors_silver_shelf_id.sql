
    
    

select
    shelf_id as unique_field,
    count(*) as n_records

from "warehouse"."main_silver"."sensors_silver"
where shelf_id is not null
group by shelf_id
having count(*) > 1


