
      update "warehouse"."snapshot"."stores_snapshot" as DBT_INTERNAL_TARGET
    set dbt_valid_to = DBT_INTERNAL_SOURCE.dbt_valid_to
    from "stores_snapshot__dbt_tmp20251006121200678643" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_scd_id::text = DBT_INTERNAL_TARGET.dbt_scd_id::text
      and DBT_INTERNAL_SOURCE.dbt_change_type::text in ('update'::text, 'delete'::text)
      
        and DBT_INTERNAL_TARGET.dbt_valid_to is null;
      

    insert into "warehouse"."snapshot"."stores_snapshot" ("store_id", "store_code", "name", "channel", "region", "state", "latitude", "longitude", "open_dt", "close_dt", "ingestion_ts", "dbt_updated_at", "dbt_valid_from", "dbt_valid_to", "dbt_scd_id")
    select DBT_INTERNAL_SOURCE."store_id",DBT_INTERNAL_SOURCE."store_code",DBT_INTERNAL_SOURCE."name",DBT_INTERNAL_SOURCE."channel",DBT_INTERNAL_SOURCE."region",DBT_INTERNAL_SOURCE."state",DBT_INTERNAL_SOURCE."latitude",DBT_INTERNAL_SOURCE."longitude",DBT_INTERNAL_SOURCE."open_dt",DBT_INTERNAL_SOURCE."close_dt",DBT_INTERNAL_SOURCE."ingestion_ts",DBT_INTERNAL_SOURCE."dbt_updated_at",DBT_INTERNAL_SOURCE."dbt_valid_from",DBT_INTERNAL_SOURCE."dbt_valid_to",DBT_INTERNAL_SOURCE."dbt_scd_id"
    from "stores_snapshot__dbt_tmp20251006121200678643" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_change_type::text = 'insert'::text;


  