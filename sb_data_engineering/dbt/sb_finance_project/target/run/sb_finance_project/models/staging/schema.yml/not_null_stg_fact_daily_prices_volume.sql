
    
    select
      count(*) as failures,
      count(*) != 0 as should_warn,
      count(*) != 0 as should_error
    from (
      
    
  
    
    



select volume
from `gobierno_datos_olap`.`stg_fact_daily_prices`
where volume is null



  
  
    ) dbt_internal_test