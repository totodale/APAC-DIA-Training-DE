
  
    
    
      
    

    create  table
      "warehouse"."main_silver"."orders_header_silver__dbt_tmp"
  
  (
    order_id bigint not null unique,
    order_ts timestamp not null,
    date date not null,
    customer_id bigint not null unique,
    channel bigint not null,
    payment_method TEXT not null,
    coupon_code TEXT not null,
    channel_1 bigint not null,
    currency TEXT not null,
    isDeleted TEXT not null,
    ingestion_ts timestamp not null
    
    )
 ;
    insert into "warehouse"."main_silver"."orders_header_silver__dbt_tmp" 
  (
    
      
      order_id ,
    
      
      order_ts ,
    
      
      date ,
    
      
      customer_id ,
    
      
      channel ,
    
      
      payment_method ,
    
      
      coupon_code ,
    
      
      channel_1 ,
    
      
      currency ,
    
      
      isDeleted ,
    
      
      ingestion_ts 
    
  )
 (
      
    select order_id, order_ts, date, customer_id, channel, payment_method, coupon_code, channel_1, currency, isDeleted, ingestion_ts
    from (
        
select
    cast(order_id as bigint) as order_id,
    cast(order_ts as datetime) as order_ts,
    cast(order_dt_local as date) as date,
    cast(customer_id as bigint) as customer_id,
    cast(channel as bigint) as channel,
    trim(payment_method) as payment_method,
    trim(coupon_code) as coupon_code,
    cast(shipping_fee as bigint) as channel,
    trim(currency) as currency,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts
from "warehouse"."main"."orders_header"
    ) as model_subq
    );
  
  