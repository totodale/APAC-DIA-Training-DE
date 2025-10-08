
select
    cast(date as datetime) as date,
    currency,
    cast(rate_to_aud as double) as rate_to_aud,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts
from "warehouse"."main"."exchange_rates"