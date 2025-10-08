
    
    



select ingestion_ts
from "warehouse"."main_silver"."stores_silver"
where ingestion_ts is null


