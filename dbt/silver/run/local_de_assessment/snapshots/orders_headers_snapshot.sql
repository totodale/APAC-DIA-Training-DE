
      update "warehouse"."snapshot"."orders_header_snapshot" as DBT_INTERNAL_TARGET
    set dbt_valid_to = DBT_INTERNAL_SOURCE.dbt_valid_to
    from "orders_header_snapshot__dbt_tmp20251006121159998637" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_scd_id::text = DBT_INTERNAL_TARGET.dbt_scd_id::text
      and DBT_INTERNAL_SOURCE.dbt_change_type::text in ('update'::text, 'delete'::text)
      
        and DBT_INTERNAL_TARGET.dbt_valid_to is null;
      

    insert into "warehouse"."snapshot"."orders_header_snapshot" ("order_id", "order_ts", "order_dt_local", "customer_id", "store_id", "channel", "payment_method", "coupon_code", "shipping_fee", "currency", "ingestion_ts", "dbt_updated_at", "dbt_valid_from", "dbt_valid_to", "dbt_scd_id")
    select DBT_INTERNAL_SOURCE."order_id",DBT_INTERNAL_SOURCE."order_ts",DBT_INTERNAL_SOURCE."order_dt_local",DBT_INTERNAL_SOURCE."customer_id",DBT_INTERNAL_SOURCE."store_id",DBT_INTERNAL_SOURCE."channel",DBT_INTERNAL_SOURCE."payment_method",DBT_INTERNAL_SOURCE."coupon_code",DBT_INTERNAL_SOURCE."shipping_fee",DBT_INTERNAL_SOURCE."currency",DBT_INTERNAL_SOURCE."ingestion_ts",DBT_INTERNAL_SOURCE."dbt_updated_at",DBT_INTERNAL_SOURCE."dbt_valid_from",DBT_INTERNAL_SOURCE."dbt_valid_to",DBT_INTERNAL_SOURCE."dbt_scd_id"
    from "orders_header_snapshot__dbt_tmp20251006121159998637" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_change_type::text = 'insert'::text;


  