
  
    
    
      
    

    create  table
      "warehouse"."main_silver"."customers_silver__dbt_tmp"
  
  (
    customer_id bigint not null,
    natural_key TEXT not null,
    first_name TEXT not null,
    last_name TEXT not null,
    full_name varchar not null,
    email TEXT not null,
    phone TEXT not null,
    address_line1 TEXT not null,
    address_line2 TEXT,
    city TEXT not null,
    state_region TEXT not null,
    postcode TEXT not null,
    country_code TEXT not null,
    latitude double not null,
    longitude double not null,
    birth_date date not null,
    join_ts timestamp not null,
    is_vip boolean not null,
    gdpr_consent boolean not null,
    ingestion_ts timestamp not null
    
    )
 ;
    insert into "warehouse"."main_silver"."customers_silver__dbt_tmp" 
  (
    
      
      customer_id ,
    
      
      natural_key ,
    
      
      first_name ,
    
      
      last_name ,
    
      
      full_name ,
    
      
      email ,
    
      
      phone ,
    
      
      address_line1 ,
    
      
      address_line2 ,
    
      
      city ,
    
      
      state_region ,
    
      
      postcode ,
    
      
      country_code ,
    
      
      latitude ,
    
      
      longitude ,
    
      
      birth_date ,
    
      
      join_ts ,
    
      
      is_vip ,
    
      
      gdpr_consent ,
    
      
      ingestion_ts 
    
  )
 (
      
    select customer_id, natural_key, first_name, last_name, full_name, email, phone, address_line1, address_line2, city, state_region, postcode, country_code, latitude, longitude, birth_date, join_ts, is_vip, gdpr_consent, ingestion_ts
    from (
        
select
    cast(customer_id as bigint) as customer_id,
    trim(natural_key) as natural_key,
    trim(first_name) as first_name,
    trim(last_name) as last_name,
    concat(first_name,' ',last_name) as full_name,
    trim(email) as email,
    trim(phone) as phone,
    trim(address_line1) as address_line1, 
    trim(address_line2) as address_line2, 
    trim(city) as city, 
    trim(state_region) as state_region, 
    trim(postcode) as postcode, 
    trim(country_code) as country_code,
    cast(latitude as double) as latitude,
    cast(longitude as double) as longitude,
    cast(birth_date as date) as birth_date,
    cast(join_ts as timestamp) as join_ts,
    cast(is_vip as boolean) as is_vip,
    cast(gdpr_consent as boolean) as gdpr_consent,
    cast(ingestion_ts as datetime) as ingestion_ts
 from "warehouse"."main"."customers"
    ) as model_subq
    );
  
  