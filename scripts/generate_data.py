# Generate synthetic raw data locally with controlled edge cases.
# Usage: python scripts/generate_data.py --seed 42 --out data_raw
import argparse, os, pathlib, random
from datetime import datetime, timedelta, date
import numpy as np
from faker import Faker
from mimesis import Person, Address, Datetime
import rstr
import pyarrow as pa
import pyarrow.parquet as pq
import xlsxwriter
import json

def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=int, default=42)
    ap.add_argument('--out', type=str, default='data_raw')
    return ap.parse_args()

def ensure_dir(p): pathlib.Path(p).mkdir(parents=True, exist_ok=True)

def main():
    args = parse_args()
    random.seed(args.seed); np.random.seed(args.seed)
    out = pathlib.Path(args.out); ensure_dir(out)

    # Minimal sample generation (expand to full volumes per docs)
    #Customers
    fake = Faker('en_AU')
    customers_path = out/'customers.csv'
    with customers_path.open('w', encoding='utf-8') as f:
        f.write('customer_id,natural_key,first_name,last_name,email,phone,address_line1,address_line2,city,state_region,postcode,country_code,latitude,longitude,birth_date,join_ts,is_vip,gdpr_consent\n')
        for i in range(1, 80001):  # TODO raise to 80_000
            nk = 'CUST-' + rstr.rstr('A-Z0-9', 8)
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = fake.email() if random.random()>0.1 else 'bad_email'
            lat = -44 + random.random()*10; lon = 112 + random.random()*40
            birth = date(1960,1,1) + timedelta(days=random.randint(0, 20000))
            join_ts = datetime(2024,1,1) + timedelta(days=random.randint(0, 400), seconds=random.randint(0, 86399))
            f.write(f"{i},{nk},{fake.first_name()},{fake.last_name()},{email},{fake.phone_number().replace(',',' ')},{fake.street_address().replace(',',' ')},,{fake.city().replace(',',' ')},{fake.state_abbr()},{fake.postcode()},AU,{lat:.6f},{lon:.6f},{birth.isoformat()},{join_ts.isoformat()},{str(random.random()<0.15)},{str(random.random()>0.05)}\n")

    #Products
    fake = Faker('en_AU')
    #mime = Person(')
    products_path = out/'products.csv'
    with products_path.open('w', encoding='utf-8') as f:
        f.write('product_id,sku,name,category,subcategory,current_price,currency,is_discontinued,introduced_dt,discontinued_dt\n')
        for i in range(1, 25001):  # TODO raise to 80_000
            sku = 'SKU-' + rstr.rstr('[A-Z0-9]',8)
            category = fake.administrative_unit()
            sub_category = fake.administrative_unit()
            current_price =  random.uniform(0,10000) #if random.random()>0.05 else 0.00
            currency = fake.currency_name()
            is_discontinued = fake.boolean()
            introduced_dt = fake.date_between_dates(date_start=datetime(2000,1,1), date_end=datetime(2025,12,31))
            discontinued_dt = fake.date_between(start_date = introduced_dt, end_date = introduced_dt + timedelta(days=365)) #if random.random()>0.1 else '1900-1-1'
            f.write(f"{i},{sku},{fake.name()},{category},{sub_category},{current_price},{currency},{is_discontinued},{introduced_dt},{discontinued_dt}\n")
    
     #Stores
    fake = Faker('en_AU')
    stores_path = out/'stores.csv'
    with stores_path.open('w', encoding='utf-8') as f:
        f.write('store_id,store_code,name,channel,region,state,latitude,longitude,open_dt,close_dt\n')
        for i in range(1, 5001):  
            store_code = fake.cryptocurrency_code()
            name = fake.name()
            channel = fake.area_code()
            region = fake.administrative_unit()
            state = fake.state()
            latitude = -44 + random.random()*10 if random.random()>0.05 else 0
            longitude = 112 + random.random()*40 if random.random()>0.05 else 0 #112 + random.random()*40 if random.random()>0.05 else 0
            open_dt = fake.date_between_dates(date_start=datetime(2000,1,1), date_end=datetime(2025,12,31))
            close_dt = fake.date_between(start_date = open_dt, end_date = open_dt + timedelta(days=720))
            f.write(f"{i},{store_code},{name},{channel},{region},{state},{latitude},{longitude},{open_dt},{close_dt}\n")
    
     #Suppliers
    fake = Faker('en_AU')
    suppliers_path = out/'suppliers.csv'
    with suppliers_path.open('w', encoding='utf-8') as f:
        f.write('supplier_id,supplier_code,name,country_code,lead_time_days,preferred\n')
        for i in range(1, 8001):  
            supplier_code = fake.area_code()
            name = fake.name()
            country_code = fake.country_code()
            lead_time_days = fake.numerify()
            preferred = fake.boolean()
            f.write(f"{i},{supplier_code},{name},{country_code},{lead_time_days},{preferred}\n")
    
    #Orders Header
    fake = Faker('en_AU')
    orders_header_path = out/'orders_header.csv'
    with orders_header_path.open('w', encoding='utf-8') as f:
        f.write('order_id,order_ts,order_dt_local,customer_id,store_id,channel,payment_method,coupon_code,shipping_fee,currency\n')
        for i in range(1, 1000001):  
            order_ts = datetime(2024,1,1) + timedelta(days=random.randint(0, 400), seconds=random.randint(0, 86399))
            order_dt_local = fake.date_between(start_date = order_ts, end_date = order_ts)
            customer_id = i #if random.random()>0.1 else 0
            store_id =  i #if random.random()>0.1 else 0
            channel = fake.area_code()
            payment_method = fake.currency_code()
            coupon_code = fake.currency_code()
            shipping_fee = random.uniform(0,10000)
            currency = fake.currency_name()
            f.write(f"{i},{order_ts},{order_dt_local},{customer_id},{store_id},{channel},{payment_method},{coupon_code},{shipping_fee},{currency}\n")
    
    #Orders Lines
    fake = Faker('en_AU')
    orders_lines_path = out/'orders_lines.csv'
    with orders_lines_path.open('w', encoding='utf-8') as f:
        f.write('order_id,line_number,product_id,qty,unit_price,line_discount_pct,tax_pct\n')
        for i in range(1, 4000001):  
            line_number = fake.random_number()
            product_id = i #if random.random()>0.1 else 0
            qty = fake.numerify()
            unit_price = random.uniform(0,10000)
            line_discount_pct = random.uniform(0.00,0.30)
            tax_pct = random.uniform(0.00,0.20)
            f.write(f"{i},{line_number},{product_id},{qty},{unit_price},{line_discount_pct},{tax_pct}\n")
    
    #Events (json format)
    
   # fake = Faker('en_AU')
   # headers ={
   #         "event_id": "",
   #         "event_ts": "",
   #         "event_type": "",
   #         "user_id": "",
   #         "session_id": ""
   #         }
   # events_path = out/'events.json'
   # with events_path.open('w', encoding='utf-8') as f:
   #     for i in range(1, 1001):  
   #         headers['event_id'] = "udonis"
   #         headers['event_ts'] = "udonis"
   #         headers['event_type'] = "udonis"
   #         headers['user_id'] = "udonis"
   #         headers['session_id'] = "udonis"
   #     f.write(json.dump(headers,f,indent=4))
    
    #Sensors
    fake = Faker('en_AU')
    sensors_path = out/'sensors.csv'
    with sensors_path.open('w', encoding='utf-8') as f:
        f.write('sensor_ts,store_id,shelf_id,temperature_c,humidity_pct,battery_mv\n')
        for i in range(1, 4000001):  
            sensor_ts = fake.date_between_dates(date_start=datetime(2000,1,1), date_end=datetime(2025,12,31)) #if random.random()>0.1 else datetime(1999,1,1)
            store_id = i
            shelf_id = i
            temperature_c =  random.uniform(10,40) if random.random()>0.05 else 0
            humidity_pct = random.uniform(0,100) if random.random()>0.05 else 0
            battery_mv = fake.numerify()
            f.write(f"{sensor_ts},{store_id},{shelf_id},{temperature_c},{humidity_pct},{battery_mv}\n")
 
    #Exchange Rates
    fake = Faker('en_AU')
    exchange_rates_path = out/'exchange_rates.csv'
    with exchange_rates_path.open('w', encoding='utf-8') as f:
        f.write('date,currency,rate_to_aud\n')
        for i in range(1, 1101):  
            date_var = fake.date()
            currency = fake.currency_name()
            rate_to_aud = random.uniform(0,10000)
            f.write(f"{date_var},{currency},{rate_to_aud}\n")


    # Shipments parquet sample
    tbl = pa.table({
        'shipment_id': pa.array(range(1, 10001), type=pa.int64()),
        'order_id': pa.array(range(1, 10001), type=pa.int64()),
        'carrier': pa.array(['AUSPOST']*10000, type=pa.string()),
        'shipped_at': pa.array([datetime(2024,1,1)+timedelta(days=i%90) for i in range(10000)], type=pa.timestamp('us')),
        'delivered_at': pa.array([datetime(2024,1,2)+timedelta(days=i%90) for i in range(10000)], type=pa.timestamp('us')),
        'ship_cost': pa.array([1995]*10000, type=pa.int64()), #cast(pa.decimal128(12,2)
    })
    pq.write_table(tbl, out/'shipments.parquet', compression='snappy')
    
    #returns
    fake = Faker('en_AU')
    returns_path = out/'returns.csv'
    with returns_path.open('w', encoding='utf-8') as f:
        f.write('return_id,order_id,product_id,return_ts,qty,reason\n')
        for i in range(1, 100001):  
            return_id = i
            order_id = i
            product_id = i
            return_ts = fake.date_between_dates(date_start=datetime(2000,1,1), date_end=datetime(2025,12,31))
            qty = fake.numerify()
            reason = 'Quality Issues' if random.random()>0.3 else 'Factory Defect' if random.random()>0.3 else 'Not Satisfied' if random.random()>0.4 else 'Reason Not Specified'
            f.write(f"{return_id},{order_id},{product_id},{return_ts},{qty},{reason}\n")

    print(f"✅ Sample raw written to {out}. Expand to required volumes per /docs.")
if __name__ == '__main__':
    main()
