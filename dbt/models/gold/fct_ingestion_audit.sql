{{
    config(materialized='table')
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
    COALESCE(a.row_count - b.total_reject_count,a.row_count) as total_valid_rows
FROM manifest_data AS a
LEFT JOIN {{ ref('rejects_count_total_silver') }} AS b
    ON a.table_name = b.table_name