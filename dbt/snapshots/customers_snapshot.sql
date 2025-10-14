{% snapshot customers_snapshot %}
{{
  config(
    target_schema='snapshot',
    unique_key='customer_id',
    strategy='check',
    check_cols=['first_name','last_name','email','phone','address_line1','city','state_region','postcode','country_code','latitude','longitude','birth_date','join_ts']
  )
}}
select * from {{ ref('stg_customers') }}
{% endsnapshot %}
