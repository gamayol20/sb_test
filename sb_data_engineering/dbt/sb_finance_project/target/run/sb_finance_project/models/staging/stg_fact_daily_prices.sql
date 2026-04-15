

  create or replace view `gobierno_datos_olap`.`stg_fact_daily_prices` 
  
    
  
  
    
    
  as (
    select
    ticker,
    trade_date,
    open_price,
    high_price,
    low_price,
    close_price,
    volume
from gobierno_datos_olap.fact_daily_prices
    
  )
      
      
                    -- end_of_sql
                    
                    