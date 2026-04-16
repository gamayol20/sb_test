select
    ticker,
    toYear(trade_date) as year,
    toMonth(trade_date) as month,
    avg(open_price) as avg_open_price,
    avg(close_price) as avg_close_price,
    avg(volume) as avg_volume
from gobierno_datos_olap.fact_daily_prices
group by
    ticker,
    toYear(trade_date),
    toMonth(trade_date)