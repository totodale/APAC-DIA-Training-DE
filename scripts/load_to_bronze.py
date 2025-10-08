# Ingest raw files into Bronze (Parquet + Delta), with schema validation, partitioning,
# rejects, and manifest tracking in DuckDB.
# Usage: python scripts/load_to_bronze.py --raw data_raw --lake lake --manifest duckdb/warehouse.duckdb
import argparse, pathlib, os, hashlib, json, datetime as dt
import duckdb
import pyarrow as pa
import pyarrow.csv as pacsv
import pyarrow.dataset as pads
import pyarrow.parquet as pq
from datetime import datetime
#from schemas.schemas import customers_schema, products_schema, stores_schema, suppliers_schema, orders_header_schema, orders_lines_schema, sensors_schema

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
        CREATE OR REPLACE TABLE manifest_processed_files (
            src_path TEXT PRIMARY KEY,
            processed_at TIMESTAMP,
            row_count BIGINT
        )
    ''')

def ingestToTable(conn, tableName):
    fileName = f"data_raw/{tableName}.csv"
    defaultValue = datetime.now()
    conn.execute(f"CREATE OR REPLACE TABLE {tableName} AS SELECT * FROM read_csv('{fileName}')")
    conn.execute(f"ALTER TABLE {tableName} ADD (ingestion_ts datetime DEFAULT '{defaultValue}, src_filename string DEFAULT '{fileName}')")

def ingestToTableParquet(conn, tableName):
    fileName = f"data_raw/{tableName}.parquet"
    defaultValue = datetime.now()
    conn.execute(f"CREATE OR REPLACE TABLE {tableName} AS SELECT * FROM read_parquet('{fileName}')")
    conn.execute(f"ALTER TABLE {tableName} ADD (ingestion_ts datetime DEFAULT '{defaultValue}, src_filename string DEFAULT '{fileName}')")


def already_processed(conn, p): return conn.execute("SELECT 1 FROM manifest_processed_files WHERE src_path = ?", [str(p)]).fetchone() is not None
def mark_processed(conn, p, n): conn.execute("INSERT OR REPLACE INTO manifest_processed_files VALUES (?, ?, ?)", [str(p), dt.datetime.utcnow(), n])

def write_parquet_partitioned(table, base_path, partitioning=None):
    pads.write_dataset(table, base_dir=str(base_path), format='parquet', partitioning=partitioning, existing_data_behavior='overwrite_or_ignore')

def write_delta(table, base_path, mode='append', partition_by=None, merge_schema=False):
    if write_deltalake is None:
        raise RuntimeError('deltalake not installed')
    write_deltalake(str(base_path), table, mode=mode, partition_by=partition_by or [])

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
    ingestToTable(conn,'customers')
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
    ingestToTable(conn,'products')
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
    ingestToTable(conn,'stores')
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
    ingestToTable(conn,'suppliers')
    mark_processed(conn, src, len(tbl))

def load_orders_header(raw_root, lake_root, conn):
    src = raw_root/'orders_header.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(orders_header_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    pq_base = lake_root/'bronze'/'parquet'/'orders_header'
    dl_base = lake_root/'bronze'/'delta'/'orders_header'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    ingestToTable(conn,'orders_header')
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
    ingestToTable(conn,'orders_lines')
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
    ingestToTable(conn,'sensors')
    mark_processed(conn, src, len(tbl))

def load_exchange_rates(raw_root, lake_root, conn):
    src = raw_root/'exchange_rates.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(exchange_rates_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    pq_base = lake_root/'bronze'/'parquet'/'exchange_rates'
    dl_base = lake_root/'bronze'/'delta'/'exchange_rates'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    ingestToTable(conn,'exchange_rates')
    mark_processed(conn, src, len(tbl))
    
def load_shipments(raw_root, lake_root, conn):
    src = raw_root/'shipments.parquet'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pq.read_table(src) #ReadOptions(encoding='utf-8')
    tbl = tbl.cast(shipments_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    pq_base = lake_root/'bronze'/'parquet'/'shipements'
    dl_base = lake_root/'bronze'/'delta'/'shipments'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    ingestToTableParquet(conn,'shipments')
    mark_processed(conn, src, len(tbl))

def load_returns(raw_root, lake_root, conn):
    src = raw_root/'returns.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(returns_day1_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    pq_base = lake_root/'bronze'/'parquet'/'returns'
    dl_base = lake_root/'bronze'/'delta'/'returns'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    ingestToTable(conn,'returns')
    mark_processed(conn, src, len(tbl))

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
    pa.field("ship_cost", pa.int64()), #decimal128(12, 2)
])

returns_day1_schema = pa.schema([
    pa.field("return_id", pa.int64()),
    pa.field("order_id", pa.int64()),
    pa.field("product_id", pa.int64()),
    pa.field("return_ts", pa.timestamp("us")),
    pa.field("qty", pa.int32()),
    pa.field("reason", pa.string()),
])


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
    load_orders_header(raw_root, lake_root, conn)
    load_orders_lines(raw_root, lake_root, conn)
    load_sensors(raw_root, lake_root, conn)
    load_exchange_rates(raw_root, lake_root, conn)
    load_shipments(raw_root, lake_root, conn)
    load_returns(raw_root, lake_root, conn)

    print("✅ Bronze load completed for implemented loaders (extend for all tables).")

if __name__ == '__main__':
    main()