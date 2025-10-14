{% snapshot orders_header_snapshot %}
{{
  config(
    target_schema='snapshot',
    unique_key='order_id',
    strategy='check',
    check_cols=['channel','payment_method','coupon_code','shipping_fee','currency']
  )
}}
select * from {{ ref('stg_orders_header') }}
{% endsnapshot %}
