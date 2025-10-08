
      update "warehouse"."snapshot"."suppliers_snapshot" as DBT_INTERNAL_TARGET
    set dbt_valid_to = DBT_INTERNAL_SOURCE.dbt_valid_to
    from "suppliers_snapshot__dbt_tmp20251006121200995684" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_scd_id::text = DBT_INTERNAL_TARGET.dbt_scd_id::text
      and DBT_INTERNAL_SOURCE.dbt_change_type::text in ('update'::text, 'delete'::text)
      
        and DBT_INTERNAL_TARGET.dbt_valid_to is null;
      

    insert into "warehouse"."snapshot"."suppliers_snapshot" ("supplier_id", "supplier_code", "name", "country_code", "lead_time_days", "preferred", "ingestion_ts", "dbt_updated_at", "dbt_valid_from", "dbt_valid_to", "dbt_scd_id")
    select DBT_INTERNAL_SOURCE."supplier_id",DBT_INTERNAL_SOURCE."supplier_code",DBT_INTERNAL_SOURCE."name",DBT_INTERNAL_SOURCE."country_code",DBT_INTERNAL_SOURCE."lead_time_days",DBT_INTERNAL_SOURCE."preferred",DBT_INTERNAL_SOURCE."ingestion_ts",DBT_INTERNAL_SOURCE."dbt_updated_at",DBT_INTERNAL_SOURCE."dbt_valid_from",DBT_INTERNAL_SOURCE."dbt_valid_to",DBT_INTERNAL_SOURCE."dbt_scd_id"
    from "suppliers_snapshot__dbt_tmp20251006121200995684" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_change_type::text = 'insert'::text;


  