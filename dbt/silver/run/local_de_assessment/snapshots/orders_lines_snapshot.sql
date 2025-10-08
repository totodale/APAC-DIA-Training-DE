
      update "warehouse"."snapshot"."orders_lines_snapshot" as DBT_INTERNAL_TARGET
    set dbt_valid_to = DBT_INTERNAL_SOURCE.dbt_valid_to
    from "orders_lines_snapshot__dbt_tmp20251006121200018701" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_scd_id::text = DBT_INTERNAL_TARGET.dbt_scd_id::text
      and DBT_INTERNAL_SOURCE.dbt_change_type::text in ('update'::text, 'delete'::text)
      
        and DBT_INTERNAL_TARGET.dbt_valid_to is null;
      

    insert into "warehouse"."snapshot"."orders_lines_snapshot" ("order_id", "line_number", "product_id", "qty", "unit_price", "line_discount_pct", "tax_pct", "ingestion_ts", "dbt_updated_at", "dbt_valid_from", "dbt_valid_to", "dbt_scd_id")
    select DBT_INTERNAL_SOURCE."order_id",DBT_INTERNAL_SOURCE."line_number",DBT_INTERNAL_SOURCE."product_id",DBT_INTERNAL_SOURCE."qty",DBT_INTERNAL_SOURCE."unit_price",DBT_INTERNAL_SOURCE."line_discount_pct",DBT_INTERNAL_SOURCE."tax_pct",DBT_INTERNAL_SOURCE."ingestion_ts",DBT_INTERNAL_SOURCE."dbt_updated_at",DBT_INTERNAL_SOURCE."dbt_valid_from",DBT_INTERNAL_SOURCE."dbt_valid_to",DBT_INTERNAL_SOURCE."dbt_scd_id"
    from "orders_lines_snapshot__dbt_tmp20251006121200018701" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_change_type::text = 'insert'::text;


  