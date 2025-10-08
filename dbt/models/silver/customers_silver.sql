{{ config(
    materialized='table',
    contract={'enforced': true}
)}}
select
    cast(customer_id as bigint) as customer_id,
    trim(natural_key) as natural_key,
    trim(first_name) as first_name,
    trim(last_name) as last_name,
    concat(first_name,' ',last_name) as full_name,
    trim(email) as email,
    trim(phone) as phone,
    trim(address_line1) as address_line1, 
    trim(address_line2) as address_line2, 
    trim(city) as city, 
    trim(state_region) as state_region, 
    trim(postcode) as postcode, 
    trim(country_code) as country_code,
    cast(latitude as double) as latitude,
    cast(longitude as double) as longitude,
    cast(birth_date as date) as birth_date,
    cast(join_ts as timestamp) as join_ts,
    cast(is_vip as boolean) as is_vip,
    cast(gdpr_consent as boolean) as gdpr_consent,
    cast(ingestion_ts as datetime) as ingestion_ts
 from {{ source('main','customers') }}