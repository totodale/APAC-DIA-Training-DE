
    
    



select ingestion_ts
from "warehouse"."main_silver"."products_silver"
where ingestion_ts is null


