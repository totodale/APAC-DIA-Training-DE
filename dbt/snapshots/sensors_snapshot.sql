{% snapshot sensors_snapshot %}
{{
  config(
    target_schema='snapshot',
    unique_key='store_id',
    strategy='check',
    check_cols=['temperature_c','humidity_pct','battery_mv']
  )
}}
select * from {{ source('main','sensors') }}
{% endsnapshot %}
