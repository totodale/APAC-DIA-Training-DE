{% snapshot suppliers_snapshot %}
{{
  config(
    target_schema='snapshot',
    unique_key='supplier_id',
    strategy='check',
    check_cols=['supplier_code','name','country_code','lead_time_days']
  )
}}
select * from {{ ref('stg_suppliers') }}
{% endsnapshot %}
