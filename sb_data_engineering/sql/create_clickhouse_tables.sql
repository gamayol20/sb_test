CREATE DATABASE IF NOT EXISTS gobierno_datos_olap;

CREATE TABLE IF NOT EXISTS gobierno_datos_olap.dim_bank_info
(
    ticker String,
    company_name String,
    industry String,
    sector String,
    employee_count Nullable(Int64),
    city String,
    phone String,
    state String,
    country String,
    website String,
    address String,
    load_timestamp DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY ticker;

CREATE TABLE IF NOT EXISTS gobierno_datos_olap.fact_daily_prices
(
    ticker String,
    trade_date DateTime,
    open_price Float64,
    high_price Float64,
    low_price Float64,
    close_price Float64,
    volume Int64,
    load_timestamp DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (ticker, trade_date);

CREATE TABLE IF NOT EXISTS gobierno_datos_olap.fact_fundamentals
(
    ticker String,
    company_name String,
    assets Nullable(Float64),
    debt Nullable(Float64),
    invested_capital Nullable(Float64),
    shares_issued Nullable(Int64),
    load_timestamp DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY ticker;

CREATE TABLE IF NOT EXISTS gobierno_datos_olap.fact_holders
(
    ticker String,
    holder_date Date,
    holder String,
    shares Nullable(Int64),
    value Nullable(Float64),
    load_timestamp DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (ticker, holder_date, holder);

CREATE TABLE IF NOT EXISTS gobierno_datos_olap.fact_ratings
(
    ticker String,
    rating_date Date,
    to_grade String,
    from_grade String,
    action String,
    load_timestamp DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (ticker, rating_date);

CREATE TABLE IF NOT EXISTS gobierno_datos_olap.monthly_stock_summary
(
    ticker String,
    year UInt16,
    month UInt8,
    avg_open_price Float64,
    avg_close_price Float64,
    avg_volume Float64,
    load_timestamp DateTime DEFAULT now()
)
ENGINE = MergeTree
ORDER BY (ticker, year, month);