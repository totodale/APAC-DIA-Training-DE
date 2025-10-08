import datetime
import dlt
import numpy
import pandas
from dlt.sources.filesystem import filesystem
import pyarrow as pa
#from schemas.schemas import *
#from scripts.load_to_bronze import write_delta

import argparse, pathlib, os, hashlib, json, datetime as dt
import duckdb
import pyarrow as pa
import pyarrow.csv as pacsv
import pyarrow.dataset as pads
import pyarrow.parquet as pq

#schema

customers_schema = pa.schema([
    pa.field("customer_id", pa.int64()),
    pa.field("natural_key", pa.string()),
    pa.field("first_name", pa.string()),
    pa.field("last_name", pa.string()),
    pa.field("email", pa.string()),
    pa.field("phone", pa.string()),
    pa.field("address_line1", pa.string()),
    pa.field("address_line2", pa.string()),
    pa.field("city", pa.string()),
    pa.field("state_region", pa.string()),
    pa.field("postcode", pa.string()),
    pa.field("country_code", pa.string()),
    pa.field("latitude", pa.float64()),
    pa.field("longitude", pa.float64()),
    pa.field("birth_date", pa.date32()),
    pa.field("join_ts", pa.timestamp("us")),  # normalize TZ downstream
    pa.field("is_vip", pa.bool_()),
    pa.field("gdpr_consent", pa.bool_()),
])

products_schema = pa.schema([
    pa.field("product_id", pa.int64()),
    pa.field("sku", pa.string()),
    pa.field("name", pa.string()),
    pa.field("category", pa.string()),
    pa.field("subcategory", pa.string()),
    pa.field("current_price", pa.decimal128(12, 4)),
    pa.field("currency", pa.string()),
    pa.field("is_discontinued", pa.bool_()),
    pa.field("introduced_dt", pa.date32()),
    pa.field("discontinued_dt", pa.date32()),
])

stores_schema = pa.schema([
    pa.field("store_id", pa.int64()),
    pa.field("store_code", pa.string()),
    pa.field("name", pa.string()),
    pa.field("channel", pa.string()),
    pa.field("region", pa.string()),
    pa.field("state", pa.string()),
    pa.field("latitude", pa.float64()),
    pa.field("longitude", pa.float64()),
    pa.field("open_dt", pa.date32()),
    pa.field("close_dt", pa.date32()),
])

suppliers_schema = pa.schema([
    pa.field("supplier_id", pa.int64()),
    pa.field("supplier_code", pa.string()),
    pa.field("name", pa.string()),
    pa.field("country_code", pa.string()),
    pa.field("lead_time_days", pa.int32()),
    pa.field("preferred", pa.bool_()),
])

orders_header_schema = pa.schema([
    pa.field("order_id", pa.int64()),
    pa.field("order_ts", pa.timestamp("us")),
    pa.field("order_dt_local", pa.date32()),
    pa.field("customer_id", pa.int64()),
    pa.field("store_id", pa.int64()),
    pa.field("channel", pa.string()),
    pa.field("payment_method", pa.string()),
    pa.field("coupon_code", pa.string()),
    pa.field("shipping_fee", pa.decimal128(12, 2)),
    pa.field("currency", pa.string()),
])

orders_lines_schema = pa.schema([
    pa.field("order_id", pa.int64()),
    pa.field("line_number", pa.int32()),
    pa.field("product_id", pa.int64()),
    pa.field("qty", pa.int32()),
    pa.field("unit_price", pa.decimal128(12, 4)),
    pa.field("line_discount_pct", pa.decimal128(5, 4)),
    pa.field("tax_pct", pa.decimal128(5, 4)),
])

events_schema = pa.schema([
    pa.field("json", pa.string()),
])

sensors_schema = pa.schema([
    pa.field("sensor_ts", pa.timestamp("us")),
    pa.field("store_id", pa.int64()),
    pa.field("shelf_id", pa.string()),
    pa.field("temperature_c", pa.decimal128(5, 2)),
    pa.field("humidity_pct", pa.decimal128(5, 2)),
    pa.field("battery_mv", pa.int32()),
])

exchange_rates_schema = pa.schema([
    pa.field("date", pa.date32()),
    pa.field("currency", pa.string()),
    pa.field("rate_to_aud", pa.decimal128(18, 8)),
])

shipments_schema = pa.schema([
    pa.field("shipment_id", pa.int64()),
    pa.field("order_id", pa.int64()),
    pa.field("carrier", pa.string()),
    pa.field("shipped_at", pa.timestamp("us")),
    pa.field("delivered_at", pa.timestamp("us")),
    pa.field("ship_cost", pa.decimal128(12, 2)),
])

returns_day1_schema = pa.schema([
    pa.field("return_id", pa.int64()),
    pa.field("order_id", pa.int64()),
    pa.field("product_id", pa.int64()),
    pa.field("return_ts", pa.timestamp("us")),
    pa.field("qty", pa.int32()),
    pa.field("reason", pa.string()),
])
#load to bronze

try:
    from deltalake import write_deltalake
except Exception as e:
    write_deltalake = None

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('--raw', type=str, default='data_raw')
    ap.add_argument('--lake', type=str, default='lake')
    ap.add_argument('--manifest', type=str, default='duckdb/warehouse.duckdb')
    return ap.parse_args()

def ensure_dirs(lake_root):
    for sub in ['bronze/parquet','bronze/delta']:
        (lake_root/sub).mkdir(parents=True, exist_ok=True)
    (lake_root/'_rejects').mkdir(parents=True, exist_ok=True)

def init_manifest(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS manifest_processed_files (
            src_path TEXT PRIMARY KEY,
            processed_at TIMESTAMP,
            row_count BIGINT,
            reject_count BIGINT,
            status TEXT
        )
    ''')

def already_processed(conn, p): return conn.execute("SELECT 1 FROM manifest_processed_files WHERE src_path = ?", [str(p)]).fetchone() is not None
def mark_processed(conn, p, n): conn.execute("INSERT OR REPLACE INTO manifest_processed_files VALUES (?, ?, ?)", [str(p), dt.datetime.utcnow(), n])

def write_parquet_partitioned(table, base_path, partitioning=None):
    pads.write_dataset(table, base_dir=str(base_path), format='parquet', partitioning=partitioning, existing_data_behavior='overwrite_or_ignore')

def write_delta(table, base_path, mode='append', partition_by=None, merge_schema=False):
    if write_deltalake is None:
        raise RuntimeError('deltalake not installed')
    write_deltalake(str(base_path), table=table, mode=mode, partition_by=partition_by or [], overwrite_schema=False, engine='rust', schema_mode='merge' if merge_schema else 'fail')

def load_customers(raw_root, lake_root, conn):
    src = raw_root/'customers.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(customers_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    pq_base = lake_root/'bronze'/'parquet'/'customers'
    dl_base = lake_root/'bronze'/'delta'/'customers'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    mark_processed(conn, src, len(tbl))

def load_products(raw_root, lake_root, conn):
    src = raw_root/'products.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(products_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    pq_base = lake_root/'bronze'/'parquet'/'products'
    dl_base = lake_root/'bronze'/'delta'/'products'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    mark_processed(conn, src, len(tbl))

def load_stores(raw_root, lake_root, conn):
    src = raw_root/'stores.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(stores_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    pq_base = lake_root/'bronze'/'parquet'/'stores'
    dl_base = lake_root/'bronze'/'delta'/'stores'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    mark_processed(conn, src, len(tbl))

def load_suppliers(raw_root, lake_root, conn):
    src = raw_root/'suppliers.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(suppliers_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    pq_base = lake_root/'bronze'/'parquet'/'suppliers'
    dl_base = lake_root/'bronze'/'delta'/'suppliers'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    mark_processed(conn, src, len(tbl))

def load_orders_headers(raw_root, lake_root, conn):
    src = raw_root/'orders_headers.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(orders_header_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    pq_base = lake_root/'bronze'/'parquet'/'orders_headers'
    dl_base = lake_root/'bronze'/'delta'/'orders_headers'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    mark_processed(conn, src, len(tbl))

def load_orders_lines(raw_root, lake_root, conn):
    src = raw_root/'orders_lines.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(orders_lines_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    pq_base = lake_root/'bronze'/'parquet'/'orders_lines'
    dl_base = lake_root/'bronze'/'delta'/'orders_lines'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    mark_processed(conn, src, len(tbl))

def load_sensors(raw_root, lake_root, conn):
    src = raw_root/'sensors.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(sensors_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    pq_base = lake_root/'bronze'/'parquet'/'sensors'
    dl_base = lake_root/'bronze'/'delta'/'sensors'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    mark_processed(conn, src, len(tbl))

def main():
    args = parse_args()
    raw_root = pathlib.Path(args.raw)
    lake_root = pathlib.Path(args.lake)
    ensure_dirs(lake_root)
    pathlib.Path(args.manifest).parent.mkdir(parents=True, exist_ok=True)
    conn = duckdb.connect(args.manifest)
    conn.execute("INSTALL delta; LOAD delta;")
    init_manifest(conn)

    load_customers(raw_root, lake_root, conn)
    load_products(raw_root, lake_root, conn)
    load_stores(raw_root, lake_root, conn)
    load_suppliers(raw_root, lake_root, conn)
    load_orders_headers(raw_root, lake_root, conn)
    load_orders_lines(raw_root, lake_root, conn)
    load_sensors(raw_root, lake_root, conn)

print("✅ Bronze load completed for implemented loaders (extend for all tables).")

# Configure destinations
duckdb_dest = dlt.destinations.duckdb(
    credentials="duckdb/warehouse.duckdb"
)

parquet_dest = dlt.destinations.filesystem(
    bucket_url="lake/bronze/parquet",
    file_format="parquet"
)

#Define sources and resources:

@dlt.source(name="retail_bronze")
def retail_source(raw_path: str = "data_raw"):
    
    @dlt.resource(
        name="customers",
        write_disposition="replace",
        columns=customers_schema  # Use PyArrow schema
    )
    def load_customers():
        # Read CSV and yield data
        # DLT handles schema validation automatically
        pass
    
    @dlt.resource(
        name="orders",
        write_disposition="append",
        primary_key="order_id",
        merge_key="order_id"
    )
    def load_orders():
        # Incremental loading with automatic dedup
        pass
    
    @dlt.transformer(
        data_from=load_customers,
        write_disposition="replace"
    )
    def add_audit_columns(record):
        # Add ingestion_ts, src_filename, etc.
        return {
            **record,
            "ingestion_ts": datetime.utcnow(),
            "src_filename": dlt.current.source_state().get("file")
        }
    
    return [
        add_audit_columns,
        load_orders,
        # ... other resources
    ]
'''
#Configure data quality checks:
# Use DLT's built-in validators
@dlt.resource(
    name="customers",
    columns={
        "email": {"data_type": "text", "nullable": False},
        "customer_id": {"data_type": "bigint", "unique": True},
        "gdpr_consent": {"data_type": "bool"}
    },
    schema_contract_settings={
        "data_type": "evolve",  # Allow schema evolution
        "columns": "complete"   # But require all defined columns
    }
)

#Handle multiple destinations:

def run_bronze_pipeline():
    # Create pipeline
    pipeline = dlt.pipeline(
        pipeline_name="retail_bronze",
        destination=duckdb_dest,
        dataset_name="bronze"
    )
    
    # Load to DuckDB
    load_info = pipeline.run(retail_source())
    
    # Also write to Parquet
    pipeline.destination = parquet_dest
    pipeline.run(retail_source())
    
    # Handle Delta format separately
    write_to_delta(pipeline.last_trace.last_extract_info)
    
#Key DLT Features to Demonstrate
#1. Incremental Loading

@dlt.resource(
    name="orders",
    write_disposition="merge",
    primary_key="order_id"
)
def orders_incremental(updated_after=dlt.sources.incremental("order_ts")):
    # DLT tracks last loaded timestamp automatically
    for file in get_order_files():
        data = read_file(file)
        yield from data.filter(lambda x: x["order_ts"] > updated_after.last_value)

#Schema Evolution

# DLT handles new columns automatically
@dlt.resource(schema_contract_settings={"columns": "evolve"})
def returns_with_evolution():
    # First batch without return_reason_code
    # Second batch with return_reason_code
    # DLT adapts automatically

# 3. Error Handling
# Configure retry and error policies
@dlt.resource(
    max_retries=3,
    retry_delay=1.0
)
def sensitive_data_source():
    # DLT handles transient failures
    pass

# Access failed records
load_info = pipeline.run(source)
for package in load_info.load_packages:
    if package.jobs["failed_jobs"]:
        # Write to rejects folder
        write_rejects(package.jobs["failed_jobs"])
        
#DLT-Specific Testing
# Run DLT pipeline
python scripts/bronze_dlt_pipeline.py

# Check DLT state and schema
dlt pipeline retail_bronze info
dlt pipeline retail_bronze trace

# Verify incremental loading
dlt pipeline retail_bronze load-info

# Test schema evolution
python scripts/bronze_dlt_pipeline.py --evolve-schema

'''