{{
    config(materialized='table')
}}
SELECT 
sensor_ts as sensor_ts,
avg(temperature_c) as avg_temperatture_c,
avg(humidity_pct) as avg_humidity_pct,
from
{{ ref('sensors_silver')}}
group by sensor_ts
order by sensor_ts 