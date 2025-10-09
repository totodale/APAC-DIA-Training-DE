
  
    
    

    create  table
      "warehouse"."main"."fct_sensor_readings__dbt_tmp"
  
    as (
      
SELECT * from 
"warehouse"."main_silver"."sensors_silver"
    );
  
  