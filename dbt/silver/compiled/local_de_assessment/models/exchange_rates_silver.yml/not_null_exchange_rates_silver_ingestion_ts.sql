
    
    



select ingestion_ts
from "warehouse"."main_silver"."exchange_rates_silver"
where ingestion_ts is null


