# Generate synthetic raw data locally with controlled edge cases.
# Usage: python scripts/generate_data.py --seed 42 --out data_raw
import argparse, os, pathlib, random
from datetime import datetime, timedelta, date
import numpy as np
from faker import Faker
from mimesis import Person, Address, Datetime
import rstr

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import xlsxwriter
from pathlib import Path
import json
import random
import uuid
from datetime import datetime, timedelta


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
    invalid_count_customers_duplicate_natural_key = 0
    invalid_count_customers_bad_email = 0
    invalid_count_customers_null_address = 0
    invalid_count_customers_total = 0
    customers_path = out/'customers.csv'
    with customers_path.open('w', encoding='utf-8') as f:
        f.write('customer_id,natural_key,first_name,last_name,email,phone,address_line1,address_line2,city,state_region,postcode,country_code,latitude,longitude,birth_date,join_ts,is_vip,gdpr_consent\n')
        for i in range(1, 85001):  # TODO raise to 80_000
            nk = 'CUST-' + rstr.rstr('A-Z0-9', 8)
            if random.random()>0.02:
                nk = 'CUST-' + rstr.rstr('A-Z0-9', 8) 
            else:
                nk = 'CUST-' + rstr.rstr('A-Z0-9', 8) 
                invalid_count_customers_duplicate_natural_key = invalid_count_customers_duplicate_natural_key + 1
            email = fake.email() 
            if random.random()>0.03:
                 email = fake.email() 
            else:
                email = 'bad_email'
                invalid_count_customers_bad_email = invalid_count_customers_bad_email + 1
            lat = -44 + random.random()*10; lon = 112 + random.random()*40
            streetAddress = fake.street_address().replace(',',' ')
            if random.random()>0.03:
                streetAddress = fake.street_address().replace(',',' ') 
            else:
                streetAddress = 'null'
                invalid_count_customers_null_address = invalid_count_customers_null_address + 1
            birth = date(1960,1,1) + timedelta(days=random.randint(0, 20000))
            join_ts = datetime(2024,1,1) + timedelta(days=random.randint(0, 400), seconds=random.randint(0, 86399))
            f.write(f"{i},{nk},{fake.first_name()},{fake.last_name()},{email},{fake.phone_number().replace(',',' ')},{streetAddress},,{fake.city().replace(',',' ')},{fake.state_abbr()},{fake.postcode()},AU,{lat:.6f},{lon:.6f},{birth.isoformat()},{join_ts.isoformat()},{str(random.random()<0.15)},{str(random.random()>0.05)}\n")
    invalid_count_customers_total = invalid_count_customers_bad_email + invalid_count_customers_duplicate_natural_key + invalid_count_customers_null_address
    
    #Products
    fake = Faker('en_AU')
    products_path = out/'products.csv'
    invalid_count_products_invalid_current_price = 0
    invalid_count_products_null_discontinued_date = 0
    invalid_count_products_total = 0
    product_name = ["Shirts","Skin Care","Makeup","Vitamins and Supplements","Pants","Dresses","Motor Vehicle Parts","Activewear","Coats and Jackets","Sneakers and Boots","Arts and Crafting Materials","Shampoo and Soap","Underwear","Bedding","Cycling"]
    product_categories = ["Electronics","Apparel","Home Goods","Books","Beauty","Sports & Outdoors","Toys & Games"]
    with products_path.open('w', encoding='utf-8') as f:
        f.write('product_id,sku,name,category,subcategory,current_price,currency,is_discontinued,introduced_dt,discontinued_dt\n')
        for i in range(1, 27001):  # TODO raise to 80_000
            sku = 'SKU-' + rstr.rstr('[A-Z0-9]',8)
            name = fake.random_element(elements=product_name)
            category = fake.random_element(elements=product_categories)
            sub_category = fake.random_element(elements=product_categories)
            current_price =  random.uniform(0,10000) 
            if random.random() > 0.05:
                current_price = random.uniform(0, 10000)
            else:
                current_price = -9999
                invalid_count_products_invalid_current_price = invalid_count_products_invalid_current_price + 1
            currency = fake.currency_name()
            is_discontinued = fake.boolean()
            introduced_dt = fake.date_between_dates(date_start=datetime(2000,1,1), date_end=datetime(2025,12,31))
            discontinued_dt = fake.date_between(start_date = introduced_dt, end_date = introduced_dt + timedelta(days=365))
            if random.random() > 0.04:
                discontinued_dt = fake.date_between(start_date = introduced_dt, end_date = introduced_dt + timedelta(days=365))
            else:
                discontinued_dt = 'NULL'
                invalid_count_products_null_discontinued_date = invalid_count_products_null_discontinued_date+ 1
            f.write(f"{i},{sku},{name},{category},{sub_category},{current_price},{currency},{is_discontinued},{introduced_dt},{discontinued_dt}\n")
    invalid_count_products_total = invalid_count_products_invalid_current_price + invalid_count_products_null_discontinued_date
    
     #Stores
    fake = Faker('en_AU')
    stores_path = out/'stores.csv'
    invalid_count_stores_latitude = 0
    invalid_count_stores_longitude = 0
    invalid_count_stores_duplicate_store_code = 0
    invalid_count_stores_total = 0
    store_name = ["Zenith Finds","The Curiosity Corner","Echo & Ember","Whimsy & Wonder","Tech Trendy Mall","Cyber Cart Central","Digit Ease Emporium","Luxe Layers Beauty","Snappy Ts","The Artisan Atelier"]
    with stores_path.open('w', encoding='utf-8') as f:
        f.write('store_id,store_code,name,channel,region,state,latitude,longitude,open_dt,close_dt\n')
        for i in range(1, 5001):  
            store_code = i 
            if random.random()>0.02:
                store_code = i
            else:
                store_code = i + i
                invalid_count_stores_duplicate_store_code = invalid_count_stores_duplicate_store_code + 1
            name = fake.random_element(elements=store_name)
            channel = fake.area_code()
            region = fake.administrative_unit()
            state = fake.state()
            latitude = -44 + random.random()*10 
            if random.random()>0.05:
                latitude = -44 + random.random()*10 
            else:
                latitude = -9999
                invalid_count_stores_latitude = invalid_count_stores_latitude + 1
            longitude = 112 + random.random()*40
            if random.random()>0.05:
                longitude = 112 + random.random()*40
            else:
                longitude = -9999
                invalid_count_stores_longitude = invalid_count_stores_longitude + 1
            invalid_count_stores_total = invalid_count_stores_latitude + invalid_count_stores_longitude + invalid_count_stores_duplicate_store_code
            open_dt = fake.date_between_dates(date_start=datetime(2000,1,1), date_end=datetime(2025,12,31))
            close_dt = fake.date_between(start_date = open_dt, end_date = open_dt + timedelta(days=720))
            f.write(f"{i},{store_code},{name},{channel},{region},{state},{latitude},{longitude},{open_dt},{close_dt}\n")
    
     #Suppliers
    fake = Faker('en_AU')
    suppliers_path = out/'suppliers.csv'
    supplier_name = ["Syncee","Alibaba","Zendrop","Trendsi","Megagoods","DropCommerce"]
    with suppliers_path.open('w', encoding='utf-8') as f:
        f.write('supplier_id,supplier_code,name,country_code,lead_time_days,preferred\n')
        for i in range(1, 8001):  
            supplier_code = fake.area_code()
            name = fake.random_element(elements=supplier_name)
            country_code = fake.country_code()
            lead_time_days = fake.numerify()
            preferred = fake.boolean()
            f.write(f"{i},{supplier_code},{name},{country_code},{lead_time_days},{preferred}\n")
      
    #Orders Header
    fake = Faker('en_AU')
    orders_header_path = out/'orders_header.csv'
    invalid_count_orders_header_customer_id = 0
    invalid_count_orders_header_duplicate_order_id= 0
    invalid_count_orders_header_total = 0
    order_channels = ["Website - Direct","Mobile App","Amazon Marketplace","eBay","In-Store POS","Shopify Store","Wholesale - B2B","Social Media - Instagram","Phone Order"]
    payment_method_fake = ["Visa","MasterCard","Amex","PayPal","Apple Pay","Cash"]
    coupon_code_fake = ["Save 20%","Free Shipping","Buy 1Take 1","Earn 500 Points"]
    with orders_header_path.open('w', encoding='utf-8') as f:
        f.write('order_id,order_ts,order_dt_local,customer_id,store_id,channel,payment_method,coupon_code,shipping_fee,currency\n')
        for i in range(1, 1000001):  
            order_id = i
            if random.random()>0.01: 
                order_id = i 
            else:
                order_id = i + i
                invalid_count_orders_header_duplicate_order_id = invalid_count_orders_header_duplicate_order_id  + 1
            order_ts = datetime(2024,1,1) + timedelta(days=random.randint(0, 400), seconds=random.randint(0, 86399))
            order_dt_local = fake.date_between(start_date = order_ts, end_date = order_ts)
            customer_id = i 
            if random.random()>0.01: 
                customer_id = i 
            else:
                customer_id = -9999
                invalid_count_orders_header_customer_id = invalid_count_orders_header_customer_id  + 1
            store_id =  i           
            channel = fake.random_element(elements=order_channels)
            payment_method = fake.random_element(elements=payment_method_fake)
            coupon_code = fake.random_element(elements=coupon_code_fake)
            shipping_fee = random.uniform(0,10000)
            currency = fake.currency_name()
            f.write(f"{order_id},{order_ts},{order_dt_local},{customer_id},{store_id},{channel},{payment_method},{coupon_code},{shipping_fee},{currency}\n")
    invalid_count_orders_header_total = invalid_count_orders_header_duplicate_order_id + invalid_count_orders_header_customer_id
    
    #Orders Lines
    fake = Faker('en_AU')
    orders_lines_path = out/'orders_lines.csv'
    invalid_count_orders_lines_product_id = 0
    invalid_count_orders_lines_unit_price = 0
    invalid_count_orders_lines_total = 0
    with orders_lines_path.open('w', encoding='utf-8') as f:
        f.write('order_id,line_number,product_id,qty,unit_price,line_discount_pct,tax_pct\n')
        for i in range(1, 4000001):  
            line_number = i
            product_id = i 
            if random.random()>0.01:
                product_id = i 
            else:
                product_id = -9999
                invalid_count_orders_lines_product_id = invalid_count_orders_lines_product_id + 1
            qty = fake.numerify()
            unit_price = random.uniform(0,10000)
            if random.random()>0.01:
                unit_price = random.uniform(0,10000)
            else: 
                unit_price = 0
                invalid_count_orders_lines_unit_price = invalid_count_orders_lines_unit_price + 1
            line_discount_pct = random.uniform(0.00,0.30)
            tax_pct = random.uniform(0.00,0.20)
            f.write(f"{i},{line_number},{product_id},{qty},{unit_price},{line_discount_pct},{tax_pct}\n")
    invalid_count_orders_lines_total = invalid_count_orders_lines_product_id + invalid_count_orders_lines_unit_price
    """
# Generate all events and group by date
    for i in range(1, num_events + 1):
        if i % progress_interval == 0:
            pct = (i / num_events) * 100
            print(f"[events] Progress: {i:,}/{num_events:,} ({pct:.0f}%)")
        # Assign event to a day
            day_offset = i % days_span
            event_date = (start_datetime + timedelta(days=day_offset)).date().isoformat()
            # Build the event JSON
            envelope = {
                "event_id": f"evt-{i}",
                "event_ts": iso(start_datetime + timedelta(days=day_offset, seconds=(i * 23) % 86400)),
                "event_type": random.choice(["page_view", "add_to_cart", "purchase", "login", "logout"]),
                "user_id": random.randint(1, self.sizes["customers"]) if random.random() > 0.01 else None,
                "session_id": f"ses-{random.randint(1, 10_000_000)}",
            }
            payload = {
                "details": {
                    "path": f"/{self.fake.slug()}",
                    "meta": {"x": random.randint(0, 100)}
                }
            }
            full_event = {"envelope": envelope, "payload": payload}
            # Sometimes write malformed JSON
            if random.random() < malformed_rate:
                if random.random() < 0.5:
                    json_str = json.dumps(full_event)[:-3]  # Truncate
                else:
                    json_str = json.dumps({"payload": payload})  # Missing envelope
                if random.random() < 0.01:  # Log only 1% to avoid spam
                    self.log_anomaly("events", "malformed_json", {"index": i})
            else:
                json_str = json.dumps(full_event)
            # Add to buffer for this date
            event_buffers[event_date].append(json_str)
        # Now write all buffers to files
        print(f"[events] Writing {len(event_buffers)} date partitions to disk...")
        for event_date, json_lines in event_buffers.items():
            # Create partition directory
            partition_dir = output_base / f"event_dt={event_date}"
            ensure_dir(partition_dir)
            # This ensures ONE file per date partition
            file_path = partition_dir / "events.jsonl"
            # Write to file (all events for this date in one file)
            with file_path.open("w", encoding="utf-8") as f:
                for line in json_lines:
                    f.write(line + "\n")
    """
    #Sensors
    fake = Faker('en_AU')
    sensors_path = out/'sensors.csv'
    invalid_count_sensors_temperature = 0
    invalid_count_sensors_humidity = 0
    invalid_count_sensors_total = 0
    with sensors_path.open('w', encoding='utf-8') as f:
        f.write('sensor_ts,store_id,shelf_id,temperature_c,humidity_pct,battery_mv\n')
        for i in range(1, 4000001):  
            sensor_ts = fake.date_between_dates(date_start=datetime(2000,1,1), date_end=datetime(2025,12,31)) #if random.random()>0.1 else datetime(1999,1,1)
            store_id = i
            shelf_id = i
            temperature_c =  random.uniform(10,40) 
            if random.random()>0.05: 
               temperature_c =  random.uniform(10,40)  
            else:
                temperature_c = -9999
                invalid_count_sensors_temperature = invalid_count_sensors_temperature + 1
            humidity_pct = random.uniform(0,100) 
            if random.random()>0.03: 
                humidity_pct = random.uniform(0,100) 
            else:
                humidity_pct = -9999
                invalid_count_sensors_humidity = invalid_count_sensors_humidity + 1
            battery_mv = fake.numerify()
            f.write(f"{sensor_ts},{store_id},{shelf_id},{temperature_c},{humidity_pct},{battery_mv}\n")
    invalid_count_sensors_total = invalid_count_sensors_temperature + invalid_count_sensors_humidity
    
    # --- SETUP ---
    # Define the output directory (assuming 'out' is a Path object)
    out = Path('data_raw/') 
    # Create the directory if it doesn't exist
    out.mkdir(exist_ok=True) 

    def generate_valid_exchange_rates_excel(output_path: Path):
        """
        Generates a valid Excel (.xlsx) file using Pandas to ensure correct structure.
        """
        print(f"Generating data and writing to {output_path.name}...")
    
        # Initialize Faker for Australian locale
        fake = Faker('en_AU')
    
        # Prepare the data as a list of dictionaries
        data = []
    
        # Generate 1100 rows of fake data
        for _ in range(1, 1101):
            data.append({
                'date': fake.date(),
                # Using 'currency_code' is often better than 'currency_name' for analysis
                'currency': fake.currency_code(), 
                # Generating rates between 0.1 and 1000 for realism
                'rate_to_aud': round(random.uniform(0.1, 1000), 4) 
            })
        
        # Convert the list of dicts to a Pandas DataFrame
        tbl = pd.DataFrame(data)
    
    # Write the DataFrame to a real XLSX file, using 'openpyxl' as the engine
    # and ensuring the DataFrame index is not written as a column.
        try:
            tbl.to_excel(
                output_path, 
                sheet_name='Sheet1', 
                index=False, 
                engine='openpyxl'
            )
            print("Successfully created a valid XLSX file.")
        except ImportError:
            print("Error: 'openpyxl' is not installed. Please run 'pip install openpyxl'.")
        except Exception as e:
            print(f"An unexpected error occurred during file writing: {e}")

    # --- EXECUTION ---
    exchange_rates_path = out/'exchange_rates.xlsx'
    generate_valid_exchange_rates_excel(exchange_rates_path)
    
    # Shipments parquet sample
    tbl = pa.table({
        'shipment_id': pa.array(range(1, 10001), type=pa.int64()),
        'order_id': pa.array(range(1, 10001), type=pa.int64()),
        'carrier': pa.array(['AUSPOST']*10000, type=pa.string()),
        'shipped_at': pa.array([datetime(2024,1,1)+timedelta(days=i%90) for i in range(10000)], type=pa.timestamp('us')),
        'delivered_at': pa.array([datetime(2024,1,2)+timedelta(days=i%90) if random.random() > 0.03 else 000 for i in range(10000)], type=pa.timestamp('us')),
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
            
    #rejects
    rejects_path = out/'rejects_count.csv'
    with rejects_path.open('w', encoding='utf-8') as f:
        f.write('reason,count,table_name\n')
        f.write(f"Invalid Email Format,{invalid_count_customers_bad_email},customers\n")
        f.write(f"Duplicate Natural Key,{invalid_count_customers_duplicate_natural_key},customers\n")
        f.write(f"Null Street Address,{invalid_count_customers_null_address},customers\n")
        f.write(f"Invalid Current Price,{invalid_count_products_invalid_current_price},products\n")
        f.write(f"Null Discontinued Date,{invalid_count_products_null_discontinued_date},products\n")
        f.write(f"Invalid Latitude Value,{invalid_count_stores_latitude},stores\n")
        f.write(f"Invalid Longitude Value,{invalid_count_stores_longitude},stores\n")
        f.write(f"Duplicate Store Code Value,{invalid_count_stores_duplicate_store_code},stores\n")
        f.write(f"Invalid Customer ID Value,{invalid_count_orders_header_customer_id},orders_header\n")
        f.write(f"Duplicate Order ID,{invalid_count_orders_header_duplicate_order_id},orders_header\n")
        f.write(f"Invalid Product ID Value,{invalid_count_orders_lines_product_id},orders_lines\n")
        f.write(f"Invalid Unit Price,{invalid_count_orders_lines_unit_price},orders_lines\n")
        f.write(f"Invalid Temperature Value,{invalid_count_sensors_temperature},sensors\n")
        f.write(f"Invalid Humidity Value,{invalid_count_sensors_humidity},sensors\n")
    
    #rejects total count
    rejects_total_path = out/'rejects_count_total.csv'
    with rejects_total_path.open('w', encoding='utf-8') as f:
        f.write('table_name,total_reject_count\n')
        f.write(f"customers,{invalid_count_customers_total}\n")
        f.write(f"products,{invalid_count_products_total}\n")
        f.write(f"stores,{invalid_count_stores_total}\n")
        f.write(f"orders_header,{invalid_count_orders_header_total}\n")
        f.write(f"orders_lines,{invalid_count_orders_lines_total}\n")
        f.write(f"sensors,{invalid_count_sensors_total}\n")


    print(f"✅ Sample raw written to {out}. Expand to required volumes per /docs.\n")
    print(f"✅ Invalid Count for Bad Email Customers: {invalid_count_customers_bad_email} | Reason: Invalid Email Format")
    print(f"✅ Invalid Count for Duplicate Natural Key Customers: {invalid_count_stores_duplicate_store_code} | Reason: Duplicate Natural Key")
    print(f"✅ Invalid Count for Null Address Customers: {invalid_count_customers_null_address} | Reason: Null Street Address")
    print(f"✅ Invalid Count Total for Customers: {invalid_count_customers_total}\n")
    
    print(f"✅ Invalid Count for Invalid Current Price: {invalid_count_products_invalid_current_price} | Reason: Invalid Current Price")
    print(f"✅ Invalid Count for Null Discontinued Date: {invalid_count_products_null_discontinued_date} | Reason: Null Discontinued Date")
    print(f"✅ Invalid Count Total for Products: {invalid_count_products_total}\n")
    
    print(f"✅ Invalid Count for Latitude Errors Stores: {invalid_count_stores_latitude} | Reason: Invalid Latitude Value")
    print(f"✅ Invalid Count for Longitude Errors Stores: {invalid_count_stores_longitude} | Reason: Invalid Longitude Value")
    print(f"✅ Invalid Count for Duplicate Store Code: {invalid_count_stores_duplicate_store_code} | Reason: Duplicate Store Code")
    print(f"✅ Invalid Count Total for Stores: {invalid_count_stores_total}\n")
    
    print(f"✅ Invalid Count for Invalid Customer ID Order Headers: {invalid_count_orders_header_customer_id} | Reason: Invalid Customer ID Value")
    print(f"✅ Invalid Count for Duplicate Order ID Order Headers: {invalid_count_orders_header_duplicate_order_id} | Reason: Duplicate Order ID")
    print(f"✅ Invalid Count Total for Order Headers: {invalid_count_orders_header_total}\n")
    
    print(f"✅ Invalid Count for Invalid Product ID Orders Lines: {invalid_count_orders_lines_product_id} | Reason: Invalid Product ID Value")
    print(f"✅ Invalid Count for Unit Price Orders Lines: {invalid_count_orders_lines_unit_price} | Reason: Invalid Unit Price")
    print(f"✅ Invalid Count Total for Order Lines: {invalid_count_orders_lines_total}\n")
    
    print(f"✅ Invalid Count for Temperature Sensors: {invalid_count_sensors_temperature} | Reason: Invalid Temperature Value")
    print(f"✅ Invalid Count for Humidity Sensors: {invalid_count_sensors_humidity} | Reason: Invalid Humidity Value")
    print(f"✅ Invalid Count Total for Sensors: {invalid_count_sensors_total}")
if __name__ == '__main__':
    main()
