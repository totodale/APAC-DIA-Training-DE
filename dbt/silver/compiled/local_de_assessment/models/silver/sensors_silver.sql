
select
    cast(sensor_ts as datetime) as sensor_ts,
    cast(store_id as bigint) as store_id,
    cast(shelf_id as bigint) as shelf_id,
    cast(temperature_c as double) as temperature_c,
    cast(humidity_pct as double) as humidity_pct,
    cast(battery_mv as bigint) as battery_mv,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts
from "warehouse"."main"."sensors"