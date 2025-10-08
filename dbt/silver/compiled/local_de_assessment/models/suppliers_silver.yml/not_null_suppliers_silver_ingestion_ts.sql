
    
    



select ingestion_ts
from "warehouse"."main_silver"."suppliers_silver"
where ingestion_ts is null


