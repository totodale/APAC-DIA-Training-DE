{{
    config(materialized='table',
    contract={'enforced': true})
}}

WITH manifest_data AS (
    SELECT
        src_path,
        LEFT(
            (SUBSTRING(src_path, INSTR(src_path, '\') + 1, LENGTH(src_path))), -- Get text after last '\'
            INSTR(
                (SUBSTRING(src_path, INSTR(src_path, '\') + 1, LENGTH(src_path))), -- Find the first '.' in the file name
                '.'
            ) - 1
        ) AS table_name,
        row_count
    FROM {{ source('main','manifest_processed_files') }}
)
SELECT
    a.src_path,
    a.table_name,
    a.row_count,
    COALESCE(b.total_reject_count,0) as total_reject_count,
    COALESCE(a.row_count - b.total_reject_count,a.row_count) as total_valid_rows,
    COALESCE(c.file_size_in_bytes,0) as file_size_in_bytes,
    COALESCE(c.processing_time_in_seconds,0) as processing_time_in_seconds
FROM manifest_data AS a
LEFT JOIN {{ ref('rejects_count_total_silver') }} AS b
    ON a.table_name = b.table_name
LEFT JOIN {{ source('main','pipeline_metrics') }} AS c
    ON a.table_name = c.table_name
WHERE c.table_name not in ('rejects_count','rejects_counts_total')