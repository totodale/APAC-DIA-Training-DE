
    
    



select ingestion_ts
from "warehouse"."main_silver"."sensors_silver"
where ingestion_ts is null


