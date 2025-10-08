{{
    config(materialized='table')
}}
SELECT
ship_Cost as shipping_cost,
EXTRACT(days from (delivered_at - shipped_at)) as delivery_days,
CASE WHEN CAST(delivery_days as BigInt) < 30 THEN 'Delivered on Time'
    WHEN CAST(delivery_days as BigInt) >= 30 AND CAST(delivery_days as BigInt) < 60 THEN 'Late Delivery'
     WHEN CAST(delivery_days as BigInt) > 60 THEN 'For Return and Refund'
ELSE 'invalid delivery time' END as on_time_flag,
CASE WHEN CAST(delivery_days as BigInt) < 30 THEN 'On SLA'
     WHEN CAST(delivery_days as BigInt) >= 30 AND CAST(delivery_days as BigInt) < 60 THEN 'SLA at Risk'
    WHEN CAST(delivery_days as BigInt) > 60 THEN 'Failed SLA'
ELSE 'invalid SLA' END as SLA_compliance,
ingestion_ts as ingestion_ts
FROM {{ ref('shipments_silver')}}