
      update "warehouse"."snapshot"."sensors_snapshot" as DBT_INTERNAL_TARGET
    set dbt_valid_to = DBT_INTERNAL_SOURCE.dbt_valid_to
    from "sensors_snapshot__dbt_tmp20251006121200634416" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_scd_id::text = DBT_INTERNAL_TARGET.dbt_scd_id::text
      and DBT_INTERNAL_SOURCE.dbt_change_type::text in ('update'::text, 'delete'::text)
      
        and DBT_INTERNAL_TARGET.dbt_valid_to is null;
      

    insert into "warehouse"."snapshot"."sensors_snapshot" ("sensor_ts", "store_id", "shelf_id", "temperature_c", "humidity_pct", "battery_mv", "ingestion_ts", "dbt_updated_at", "dbt_valid_from", "dbt_valid_to", "dbt_scd_id")
    select DBT_INTERNAL_SOURCE."sensor_ts",DBT_INTERNAL_SOURCE."store_id",DBT_INTERNAL_SOURCE."shelf_id",DBT_INTERNAL_SOURCE."temperature_c",DBT_INTERNAL_SOURCE."humidity_pct",DBT_INTERNAL_SOURCE."battery_mv",DBT_INTERNAL_SOURCE."ingestion_ts",DBT_INTERNAL_SOURCE."dbt_updated_at",DBT_INTERNAL_SOURCE."dbt_valid_from",DBT_INTERNAL_SOURCE."dbt_valid_to",DBT_INTERNAL_SOURCE."dbt_scd_id"
    from "sensors_snapshot__dbt_tmp20251006121200634416" as DBT_INTERNAL_SOURCE
    where DBT_INTERNAL_SOURCE.dbt_change_type::text = 'insert'::text;


  