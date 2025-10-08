
      update "warehouse"."snapshot"."products_snapshot" as DBT_INTERNAL_TARGET
    set dbt_valid_to = DBT_INTERNAL_SOURCE.dbt_valid_to
    from "products_snapshot__dbt_tmp20251006121200010227" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_scd_id::text = DBT_INTERNAL_TARGET.dbt_scd_id::text
      and DBT_INTERNAL_SOURCE.dbt_change_type::text in ('update'::text, 'delete'::text)
      
        and DBT_INTERNAL_TARGET.dbt_valid_to is null;
      

    insert into "warehouse"."snapshot"."products_snapshot" ("product_id", "sku", "name", "category", "subcategory", "current_price", "currency", "is_discontinued", "introduced_dt", "discontinued_dt", "ingestion_ts", "dbt_updated_at", "dbt_valid_from", "dbt_valid_to", "dbt_scd_id")
    select DBT_INTERNAL_SOURCE."product_id",DBT_INTERNAL_SOURCE."sku",DBT_INTERNAL_SOURCE."name",DBT_INTERNAL_SOURCE."category",DBT_INTERNAL_SOURCE."subcategory",DBT_INTERNAL_SOURCE."current_price",DBT_INTERNAL_SOURCE."currency",DBT_INTERNAL_SOURCE."is_discontinued",DBT_INTERNAL_SOURCE."introduced_dt",DBT_INTERNAL_SOURCE."discontinued_dt",DBT_INTERNAL_SOURCE."ingestion_ts",DBT_INTERNAL_SOURCE."dbt_updated_at",DBT_INTERNAL_SOURCE."dbt_valid_from",DBT_INTERNAL_SOURCE."dbt_valid_to",DBT_INTERNAL_SOURCE."dbt_scd_id"
    from "products_snapshot__dbt_tmp20251006121200010227" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_change_type::text = 'insert'::text;


  