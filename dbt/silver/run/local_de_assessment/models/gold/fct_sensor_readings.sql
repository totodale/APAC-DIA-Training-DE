
  
    
    

    create  table
      "warehouse"."main_gold"."fct_sensor_readings__dbt_tmp"
  
    as (
      
SELECT * from 
"warehouse"."main_silver"."sensors_silver"
    );
  
  