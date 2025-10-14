{% snapshot orders_lines_snapshot %}
{{
  config(
    target_schema='snapshot',
    unique_key='order_id',
    strategy='check',
    check_cols=['line_number','qty','unit_price','line_discount_pct','tax_pct']
  )
}}
select * from {{ ref('stg_orders_lines') }}
{% endsnapshot %}
