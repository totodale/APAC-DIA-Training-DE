
    
    



select ingestion_ts
from "warehouse"."main_silver"."shipments_silver"
where ingestion_ts is null


