
  
    
    
      
    

    create  table
      "warehouse"."main_silver"."products_silver__dbt_tmp"
  
  (
    product_id bigint not null,
    sku TEXT not null,
    name TEXT not null,
    category TEXT not null,
    subcategory varchar not null,
    current_price double not null,
    currency TEXT not null,
    is_discontinued boolean not null,
    introduced_dt date not null,
    discontinued_dt date not null,
    isDeleted TEXT not null,
    ingestion_ts timestamp not null
    
    )
 ;
    insert into "warehouse"."main_silver"."products_silver__dbt_tmp" 
  (
    
      
      product_id ,
    
      
      sku ,
    
      
      name ,
    
      
      category ,
    
      
      subcategory ,
    
      
      current_price ,
    
      
      currency ,
    
      
      is_discontinued ,
    
      
      introduced_dt ,
    
      
      discontinued_dt ,
    
      
      isDeleted ,
    
      
      ingestion_ts 
    
  )
 (
      
    select product_id, sku, name, category, subcategory, current_price, currency, is_discontinued, introduced_dt, discontinued_dt, isDeleted, ingestion_ts
    from (
        
select
    cast(product_id as bigint) as product_id,
    trim(sku) as sku,
    trim(name) as name,
    trim(category) as category,
    trim(subcategory) as subcategory,
    cast(current_price as double) as current_price,
    trim(currency) as currency,
    cast(is_discontinued as boolean) as is_discontinued,
    cast(introduced_dt as date) as introduced_dt,
    cast(discontinued_dt as date) as discontinued_dt,
    'FALSE' as isDeleted,
    cast(ingestion_ts as datetime) as ingestion_ts
 from "warehouse"."main"."products"
    ) as model_subq
    );
  
  