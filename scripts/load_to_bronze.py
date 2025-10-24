# Ingest raw files into Bronze (Parquet + Delta), with schema validation, partitioning,
# rejects, and manifest tracking in DuckDB.
# Usage: python scripts/load_to_bronze.py --raw data_raw --lake lake --manifest duckdb/warehouse.duckdb
import argparse, pathlib, os, hashlib, json, datetime as dt
import duckdb
import pyarrow as pa
import pyarrow.csv as pacsv
import pyarrow.dataset as pads
import pyarrow.parquet as pq
import os, sys
import random
import time
from datetime import datetime

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from schemas.schemas import customers_schema, products_schema, stores_schema, suppliers_schema, orders_header_schema, orders_lines_schema, sensors_schema, exchange_rates_schema, shipments_schema, returns_day1_schema, rejects_count_schema, rejects_count_total_schema

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
            row_count BIGINT,
            reject_count BIGINT,
            status TEXT
        )
    ''')
    
def initTableMetrics(conn):
    conn.execute(f"CREATE OR REPLACE TABLE pipeline_metrics (table_name varchar(255),file_size_in_bytes bigint,processing_time_in_seconds double)")

def ingestRejectsCount(conn):
    fileName = f"data_raw/rejects_count.csv"
    conn.execute(f"CREATE OR REPLACE TABLE rejects_count_per_table AS SELECT * FROM read_csv('{fileName}')")

def ingestRejectsCountTotal(conn):
    fileName = f"data_raw/rejects_count_total.csv"
    conn.execute(f"CREATE OR REPLACE TABLE rejects_count_total_per_table AS SELECT * FROM read_csv('{fileName}')")

def ingestToTable(conn, tableName):
    fileName = f"data_raw/{tableName}.csv"
    defaultValue = datetime.now()
    conn.execute(f"CREATE OR REPLACE TABLE {tableName} AS SELECT * FROM read_csv('{fileName}')")
    conn.execute(f"ALTER TABLE {tableName} ADD ingestion_ts datetime DEFAULT '{defaultValue}'")
    conn.execute(f"ALTER TABLE {tableName} ADD src_filename string DEFAULT '{fileName}'")

def ingestToTableParquet(conn, tableName):
    fileName = f"data_raw/{tableName}.parquet"
    defaultValue = datetime.now()
    conn.execute(f"CREATE OR REPLACE TABLE {tableName} AS SELECT * FROM read_parquet('{fileName}')")
    conn.execute(f"ALTER TABLE {tableName} ADD ingestion_ts datetime DEFAULT '{defaultValue}'")
    conn.execute(f"ALTER TABLE {tableName} ADD src_filename string DEFAULT '{fileName}'")

def already_processed(conn, p): return conn.execute("SELECT 1 FROM manifest_processed_files WHERE src_path = ?", [str(p)]).fetchone() is not None
def mark_processed(conn, p, n): conn.execute("INSERT OR REPLACE INTO manifest_processed_files VALUES (?, ?, ?, ?, ?)", [str(p), dt.datetime.utcnow(), n,0,''])

def write_parquet_partitioned(table, base_path, partitioning=None):
    pads.write_dataset(table, base_dir=str(base_path), format='parquet', partitioning=partitioning, existing_data_behavior='overwrite_or_ignore')

def write_delta(table, base_path, mode='append', partition_by=None, merge_schema=False):
    if write_deltalake is None:
        raise RuntimeError('deltalake not installed')
    write_deltalake(str(base_path), table, mode=mode, partition_by=partition_by or [])

def load_customers(raw_root, lake_root, conn):
    start_time = time.time()
    src = raw_root/'customers.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(customers_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    fileName = "data_raw/customers.csv"
    hash_list =[]
    for i in list(range(len(tbl))):
        data = str(random.getrandbits(32))
        hash_object = hashlib.sha256()
        hash_object.update(data.encode('utf-8'))
        hash_data = hash_object.hexdigest()
        hash_list.append(hash_data)
    row_hashes = [f"{i}" for i in hash_list]
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    tbl = tbl.append_column('src_filename', pa.array([fileName]*len(tbl), type=pa.string()))
    tbl = tbl.append_column('src_hash', pa.array(row_hashes, type=pa.string()))
    pq_base = lake_root/'bronze'/'parquet'/'customers'
    dl_base = lake_root/'bronze'/'delta'/'customers'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    ingestToTable(conn,'customers')
    mark_processed(conn, src, len(tbl))
    end_time = time.time()  
    processing_time = end_time - start_time
    src_customers = raw_root/'customers.csv'
    file_size_bytes_customers = os.path.getsize(src_customers)
    conn.execute(f"INSERT INTO pipeline_metrics values('customers',{file_size_bytes_customers},{processing_time})")

def load_products(raw_root, lake_root, conn):
    start_time = time.time()
    src = raw_root/'products.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(products_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    fileName = "data_raw/products.csv"
    hash_list =[]
    for i in list(range(len(tbl))):
        data = str(random.getrandbits(32))
        hash_object = hashlib.sha256()
        hash_object.update(data.encode('utf-8'))
        hash_data = hash_object.hexdigest()
        hash_list.append(hash_data)
    row_hashes = [f"{i}" for i in hash_list]
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    tbl = tbl.append_column('src_filename', pa.array([fileName]*len(tbl), type=pa.string()))
    tbl = tbl.append_column('src_hash', pa.array(row_hashes, type=pa.string()))
    pq_base = lake_root/'bronze'/'parquet'/'products'
    dl_base = lake_root/'bronze'/'delta'/'products'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    ingestToTable(conn,'products')
    mark_processed(conn, src, len(tbl))
    end_time = time.time()  
    processing_time = end_time - start_time
    src_products = raw_root/'products.csv'
    file_size_bytes_products = os.path.getsize(src_products)
    conn.execute(f"INSERT INTO pipeline_metrics values('products',{file_size_bytes_products},{processing_time})")

def load_stores(raw_root, lake_root, conn):
    start_time = time.time()
    src = raw_root/'stores.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(stores_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    fileName = "data_raw/stores.csv"
    hash_list =[]
    for i in list(range(len(tbl))):
        data = str(random.getrandbits(32))
        hash_object = hashlib.sha256()
        hash_object.update(data.encode('utf-8'))
        hash_data = hash_object.hexdigest()
        hash_list.append(hash_data)
    row_hashes = [f"{i}" for i in hash_list]
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    tbl = tbl.append_column('src_filename', pa.array([fileName]*len(tbl), type=pa.string()))
    tbl = tbl.append_column('src_hash', pa.array(row_hashes, type=pa.string()))
    pq_base = lake_root/'bronze'/'parquet'/'stores'
    dl_base = lake_root/'bronze'/'delta'/'stores'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    ingestToTable(conn,'stores')
    mark_processed(conn, src, len(tbl))
    end_time = time.time()  
    processing_time = end_time - start_time
    src_stores = raw_root/'stores.csv'
    file_size_bytes_stores = os.path.getsize(src_stores)
    conn.execute(f"INSERT INTO pipeline_metrics values('stores',{file_size_bytes_stores},{processing_time})")

def load_suppliers(raw_root, lake_root, conn):
    start_time = time.time()
    src = raw_root/'suppliers.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(suppliers_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    fileName = "data_raw/suppliers.csv"
    hash_list =[]
    for i in list(range(len(tbl))):
        data = str(random.getrandbits(32))
        hash_object = hashlib.sha256()
        hash_object.update(data.encode('utf-8'))
        hash_data = hash_object.hexdigest()
        hash_list.append(hash_data)
    row_hashes = [f"{i}" for i in hash_list]
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    tbl = tbl.append_column('src_filename', pa.array([fileName]*len(tbl), type=pa.string()))
    tbl = tbl.append_column('src_hash', pa.array(row_hashes, type=pa.string()))
    pq_base = lake_root/'bronze'/'parquet'/'suppliers'
    dl_base = lake_root/'bronze'/'delta'/'suppliers'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    ingestToTable(conn,'suppliers')
    mark_processed(conn, src, len(tbl))
    end_time = time.time()  
    processing_time = end_time - start_time
    src_suppliers = raw_root/'suppliers.csv'
    file_size_bytes_suppliers = os.path.getsize(src_suppliers)
    conn.execute(f"INSERT INTO pipeline_metrics values('suppliers',{file_size_bytes_suppliers},{processing_time})")

def load_orders_header(raw_root, lake_root, conn):
    start_time = time.time()
    src = raw_root/'orders_header.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(orders_header_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    fileName = "data_raw/orders_header.csv"
    hash_list =[]
    for i in list(range(len(tbl))):
        data = str(random.getrandbits(32))
        hash_object = hashlib.sha256()
        hash_object.update(data.encode('utf-8'))
        hash_data = hash_object.hexdigest()
        hash_list.append(hash_data)
    row_hashes = [f"{i}" for i in hash_list]
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    tbl = tbl.append_column('src_filename', pa.array([fileName]*len(tbl), type=pa.string()))
    tbl = tbl.append_column('src_hash', pa.array(row_hashes, type=pa.string()))
    pq_base = lake_root/'bronze'/'parquet'/'orders_header'
    dl_base = lake_root/'bronze'/'delta'/'orders_header'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    ingestToTable(conn,'orders_header')
    mark_processed(conn, src, len(tbl))
    end_time = time.time()  
    processing_time = end_time - start_time
    src_orders_header = raw_root/'orders_header.csv'
    file_size_bytes_orders_header = os.path.getsize(src_orders_header)
    conn.execute(f"INSERT INTO pipeline_metrics values('orders_header',{file_size_bytes_orders_header},{processing_time})")

def load_orders_lines(raw_root, lake_root, conn):
    start_time = time.time()
    src = raw_root/'orders_lines.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(orders_lines_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    fileName = "data_raw/orders_lines.csv"
    hash_list =[]
    for i in list(range(len(tbl))):
        data = str(random.getrandbits(32))
        hash_object = hashlib.sha256()
        hash_object.update(data.encode('utf-8'))
        hash_data = hash_object.hexdigest()
        hash_list.append(hash_data)
    row_hashes = [f"{i}" for i in hash_list]
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    tbl = tbl.append_column('src_filename', pa.array([fileName]*len(tbl), type=pa.string()))
    tbl = tbl.append_column('src_hash', pa.array(row_hashes, type=pa.string()))
    pq_base = lake_root/'bronze'/'parquet'/'orders_lines'
    dl_base = lake_root/'bronze'/'delta'/'orders_lines'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    ingestToTable(conn,'orders_lines')
    mark_processed(conn, src, len(tbl))
    end_time = time.time()  
    processing_time = end_time - start_time
    src_orders_lines = raw_root/'orders_lines.csv'
    file_size_bytes_orders_lines = os.path.getsize(src_orders_lines)
    conn.execute(f"INSERT INTO pipeline_metrics values('orders_lines',{file_size_bytes_orders_lines},{processing_time})")

def load_sensors(raw_root, lake_root, conn):
    start_time = time.time()
    src = raw_root/'sensors.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(sensors_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    fileName = "data_raw/sensors.csv"
    hash_list =[]
    for i in list(range(len(tbl))):
        data = str(random.getrandbits(32))
        hash_object = hashlib.sha256()
        hash_object.update(data.encode('utf-8'))
        hash_data = hash_object.hexdigest()
        hash_list.append(hash_data)
    row_hashes = [f"{i}" for i in hash_list]
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    tbl = tbl.append_column('src_filename', pa.array([fileName]*len(tbl), type=pa.string()))
    tbl = tbl.append_column('src_hash', pa.array(row_hashes, type=pa.string()))
    pq_base = lake_root/'bronze'/'parquet'/'sensors'
    dl_base = lake_root/'bronze'/'delta'/'sensors'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    ingestToTable(conn,'sensors')
    mark_processed(conn, src, len(tbl))
    end_time = time.time()  
    processing_time = end_time - start_time
    src_sensors = raw_root/'sensors.csv'
    file_size_bytes_sensors = os.path.getsize(src_sensors)
    conn.execute(f"INSERT INTO pipeline_metrics values('sensors',{file_size_bytes_sensors},{processing_time})")

def load_exchange_rates(raw_root, lake_root, conn):
    start_time = time.time()
    src = raw_root/'exchange_rates.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(exchange_rates_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    fileName = "data_raw/exchange_rates.csv"
    hash_list =[]
    for i in list(range(len(tbl))):
        data = str(random.getrandbits(32))
        hash_object = hashlib.sha256()
        hash_object.update(data.encode('utf-8'))
        hash_data = hash_object.hexdigest()
        hash_list.append(hash_data)
    row_hashes = [f"{i}" for i in hash_list]
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    tbl = tbl.append_column('src_filename', pa.array([fileName]*len(tbl), type=pa.string()))
    tbl = tbl.append_column('src_hash', pa.array(row_hashes, type=pa.string()))
    pq_base = lake_root/'bronze'/'parquet'/'exchange_rates'
    dl_base = lake_root/'bronze'/'delta'/'exchange_rates'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    ingestToTable(conn,'exchange_rates')
    mark_processed(conn, src, len(tbl))
    end_time = time.time()  
    processing_time = end_time - start_time
    src_exchange_rates = raw_root/'exchange_rates.csv'
    file_size_bytes_exchange_rates = os.path.getsize(src_exchange_rates)
    conn.execute(f"INSERT INTO pipeline_metrics values('exchange_rates',{file_size_bytes_exchange_rates},{processing_time})")

    
def load_shipments(raw_root, lake_root, conn):
    start_time = time.time()
    src = raw_root/'shipments.parquet'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pq.read_table(src) 
    tbl = tbl.cast(shipments_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    fileName = "data_raw/shipments.csv"
    hash_list =[]
    for i in list(range(len(tbl))):
        data = str(random.getrandbits(32))
        hash_object = hashlib.sha256()
        hash_object.update(data.encode('utf-8'))
        hash_data = hash_object.hexdigest()
        hash_list.append(hash_data)
    row_hashes = [f"{i}" for i in hash_list]
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    tbl = tbl.append_column('src_filename', pa.array([fileName]*len(tbl), type=pa.string()))
    tbl = tbl.append_column('src_hash', pa.array(row_hashes, type=pa.string()))
    pq_base = lake_root/'bronze'/'parquet'/'shipements'
    dl_base = lake_root/'bronze'/'delta'/'shipments'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    ingestToTableParquet(conn,'shipments')
    mark_processed(conn, src, len(tbl))
    end_time = time.time()  
    processing_time = end_time - start_time
    src_shipments = raw_root/'shipments.parquet'
    file_size_bytes_shipments = os.path.getsize(src_shipments)
    conn.execute(f"INSERT INTO pipeline_metrics values('shipments',{file_size_bytes_shipments},{processing_time})")

def load_returns(raw_root, lake_root, conn):
    start_time = time.time()
    src = raw_root/'returns.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(returns_day1_schema, safe=False)
    now = pa.scalar(dt.datetime.utcnow(), type=pa.timestamp('us'))
    fileName = "data_raw/returns.csv"
    hash_list =[]
    for i in list(range(len(tbl))):
        data = str(random.getrandbits(32))
        hash_object = hashlib.sha256()
        hash_object.update(data.encode('utf-8'))
        hash_data = hash_object.hexdigest()
        hash_list.append(hash_data)
    row_hashes = [f"{i}" for i in hash_list]
    tbl = tbl.append_column('ingestion_ts', pa.array([now.as_py()]*len(tbl), type=pa.timestamp('us')))
    tbl = tbl.append_column('src_filename', pa.array([fileName]*len(tbl), type=pa.string()))
    tbl = tbl.append_column('src_hash', pa.array(row_hashes, type=pa.string()))
    pq_base = lake_root/'bronze'/'parquet'/'returns'
    dl_base = lake_root/'bronze'/'delta'/'returns'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    ingestToTable(conn,'returns')
    mark_processed(conn, src, len(tbl))
    end_time = time.time()  
    processing_time = end_time - start_time
    src_returns = raw_root/'returns.csv'
    file_size_bytes_returns = os.path.getsize(src_returns)
    conn.execute(f"INSERT INTO pipeline_metrics values('returns',{file_size_bytes_returns},{processing_time})")

def load_rejects_count(raw_root, lake_root, conn):
    src = raw_root/'rejects_count.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(rejects_count_schema, safe=False)
    pq_base = lake_root/'_rejects'/'parquet'/'rejects_count'
    dl_base = lake_root/'_rejects'/'delta'/'rejects_count'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    ingestToTable(conn,'rejects_count')
    mark_processed(conn, src, len(tbl))

def load_rejects_count_total(raw_root, lake_root, conn):
    src = raw_root/'rejects_count_total.csv'
    if not src.exists(): return
    if already_processed(conn, src): return
    tbl = pacsv.read_csv(src, read_options=pacsv.ReadOptions(encoding='utf-8'))
    tbl = tbl.cast(rejects_count_total_schema, safe=False)
    pq_base = lake_root/'_rejects'/'parquet'/'rejects_count_total'
    dl_base = lake_root/'_rejects'/'delta'/'rejects_count_total'
    write_parquet_partitioned(tbl, pq_base, partitioning=None)
    write_delta(tbl, dl_base, mode='append')
    ingestToTable(conn,'rejects_count_total')
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
    initTableMetrics(conn)
    
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
    load_rejects_count(raw_root, lake_root, conn)
    load_rejects_count_total(raw_root, lake_root, conn)

    print("✅ Bronze load completed for implemented loaders (extend for all tables).\n")
    
    src_customers = raw_root/'customers.csv'
    file_size_bytes_customers = os.path.getsize(src_customers)
    print(f"customers.csv file size in bytes: {file_size_bytes_customers}")
    
    src_products = raw_root/'products.csv'
    file_size_bytes_products = os.path.getsize(src_products)
    print(f"products.csv file size in bytes: {file_size_bytes_products}")
    
    src_sensors = raw_root/'sensors.csv'
    file_size_bytes_sensors = os.path.getsize(src_sensors)
    print(f"sensors.csv file size in bytes: {file_size_bytes_sensors}")
    
    src_stores = raw_root/'stores.csv'
    file_size_bytes_stores = os.path.getsize(src_stores)
    print(f"stores.csv file size in bytes: {file_size_bytes_stores}")

    src_suppliers = raw_root/'suppliers.csv'
    file_size_bytes_suppliers = os.path.getsize(src_suppliers)
    print(f"suppliers.csv file size in bytes: {file_size_bytes_suppliers}")

    src_orders_header = raw_root/'orders_header.csv'
    file_size_bytes_orders_header = os.path.getsize(src_orders_header)
    print(f"orders_header.csv file size in bytes: {file_size_bytes_orders_header}")

    src_orders_lines = raw_root/'orders_lines.csv'
    file_size_bytes_orders_lines = os.path.getsize(src_orders_lines)
    print(f"orders_lines.csv file size in bytes: {file_size_bytes_orders_lines}")

    src_exchange_rates = raw_root/'exchange_rates.csv'
    file_size_bytes_exchange_rates = os.path.getsize(src_exchange_rates)
    print(f"exchange_rates.csv file size in bytes: {file_size_bytes_exchange_rates}")

    src_shipments = raw_root/'shipments.parquet'
    file_size_bytes_shipments = os.path.getsize(src_shipments)
    print(f"shipments.parquet file size in bytes: {file_size_bytes_shipments}")
    
if __name__ == '__main__':
    main()