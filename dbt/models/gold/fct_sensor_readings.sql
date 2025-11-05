{{
    config(materialized='table',
    contract={'enforced': true})
}}
SELECT 
{{ normalize_timestamp('sensor_ts') }} as sensor_ts,
avg(temperature_c) as avg_temperature_c,
avg(humidity_pct) as avg_humidity_pct,
ingestion_ts as ingestion_ts,
src_filename as src_filename,
src_hash as src_hash
from
{{ ref('sensors_silver')}}
group by sensor_ts, ingestion_ts, src_filename, src_hash
order by sensor_ts 