{% snapshot stores_snapshot %}
{{
  config(
    target_schema='snapshot',
    unique_key='store_id',
    strategy='check',
    check_cols=['store_code','name','channel','region','state']
  )
}}
select * from {{ source('main','stores') }}
{% endsnapshot %}
