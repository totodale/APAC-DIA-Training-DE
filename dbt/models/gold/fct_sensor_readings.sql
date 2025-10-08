{{
    config(materialized='table')
}}
SELECT * from 
{{ ref('sensors_silver')}}