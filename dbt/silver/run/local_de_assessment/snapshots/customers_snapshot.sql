
      update "warehouse"."snapshot"."customers_snapshot" as DBT_INTERNAL_TARGET
    set dbt_valid_to = DBT_INTERNAL_SOURCE.dbt_valid_to
    from "customers_snapshot__dbt_tmp20251006121159986115" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_scd_id::text = DBT_INTERNAL_TARGET.dbt_scd_id::text
      and DBT_INTERNAL_SOURCE.dbt_change_type::text in ('update'::text, 'delete'::text)
      
        and DBT_INTERNAL_TARGET.dbt_valid_to is null;
      

    insert into "warehouse"."snapshot"."customers_snapshot" ("customer_id", "natural_key", "first_name", "last_name", "email", "phone", "address_line1", "address_line2", "city", "state_region", "postcode", "country_code", "latitude", "longitude", "birth_date", "join_ts", "is_vip", "gdpr_consent", "ingestion_ts", "dbt_updated_at", "dbt_valid_from", "dbt_valid_to", "dbt_scd_id")
    select DBT_INTERNAL_SOURCE."customer_id",DBT_INTERNAL_SOURCE."natural_key",DBT_INTERNAL_SOURCE."first_name",DBT_INTERNAL_SOURCE."last_name",DBT_INTERNAL_SOURCE."email",DBT_INTERNAL_SOURCE."phone",DBT_INTERNAL_SOURCE."address_line1",DBT_INTERNAL_SOURCE."address_line2",DBT_INTERNAL_SOURCE."city",DBT_INTERNAL_SOURCE."state_region",DBT_INTERNAL_SOURCE."postcode",DBT_INTERNAL_SOURCE."country_code",DBT_INTERNAL_SOURCE."latitude",DBT_INTERNAL_SOURCE."longitude",DBT_INTERNAL_SOURCE."birth_date",DBT_INTERNAL_SOURCE."join_ts",DBT_INTERNAL_SOURCE."is_vip",DBT_INTERNAL_SOURCE."gdpr_consent",DBT_INTERNAL_SOURCE."ingestion_ts",DBT_INTERNAL_SOURCE."dbt_updated_at",DBT_INTERNAL_SOURCE."dbt_valid_from",DBT_INTERNAL_SOURCE."dbt_valid_to",DBT_INTERNAL_SOURCE."dbt_scd_id"
    from "customers_snapshot__dbt_tmp20251006121159986115" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_change_type::text = 'insert'::text;


  