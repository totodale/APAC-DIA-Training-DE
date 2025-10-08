
    
    



select ingestion_ts
from "warehouse"."main_silver"."returns_silver"
where ingestion_ts is null


