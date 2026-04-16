import os
import pandas as pd
from sqlalchemy import create_engine, text

pg_host = os.getenv("POSTGRES_HOST", "localhost")
ch_host = os.getenv("CLICKHOUSE_HOST", "localhost")

pg_engine = create_engine(
    f"postgresql+psycopg2://postgres:postgres@{pg_host}:5432/gobierno_datos"
)

ch_engine = create_engine(
    f"clickhouse+http://default:clickhouse123@{ch_host}:8123/gobierno_datos_olap"
)

def load_dim_bank_info():
    query = """
        SELECT
            ticker,
            nombre_empresa AS company_name,
            industria AS industry,
            sector,
            cantidad_empleados AS employee_count,
            ciudad AS city,
            telefono AS phone,
            estado AS state,
            pais AS country,
            sitio_web AS website,
            direccion AS address
        FROM raw_informacion_basica
    """
    df = pd.read_sql(query, pg_engine)
    df.to_sql("dim_bank_info", ch_engine, if_exists="append", index=False)
    print(f"Loaded dim_bank_info: {len(df)} rows")

def load_fact_daily_prices():
    query = """
        SELECT
            ticker,
            fecha AS trade_date,
            precio_apertura AS open_price,
            precio_maximo AS high_price,
            precio_minimo AS low_price,
            precio_cierre AS close_price,
            volumen AS volume
        FROM raw_precios_diarios
    """
    df = pd.read_sql(query, pg_engine)
    df.to_sql("fact_daily_prices", ch_engine, if_exists="append", index=False)
    print(f"Loaded fact_daily_prices: {len(df)} rows")

def load_fact_fundamentals():
    query = """
        SELECT
            ticker,
            nombre_empresa AS company_name,
            activos AS assets,
            deuda AS debt,
            capital_invertido AS invested_capital,
            acciones_emitidas AS shares_issued
        FROM raw_fundamentales
    """
    df = pd.read_sql(query, pg_engine)
    df.to_sql("fact_fundamentals", ch_engine, if_exists="append", index=False)
    print(f"Loaded fact_fundamentals: {len(df)} rows")

def load_fact_holders():
    query = """
        SELECT
            ticker,
            fecha AS holder_date,
            tenedor AS holder,
            acciones AS shares,
            valor AS value
        FROM raw_tenedores
    """
    df = pd.read_sql(query, pg_engine)
    df.to_sql("fact_holders", ch_engine, if_exists="append", index=False)
    print(f"Loaded fact_holders: {len(df)} rows")

def load_fact_ratings():
    query = """
        SELECT
            ticker,
            fecha AS rating_date,
            calificacion_destino AS to_grade,
            calificacion_origen AS from_grade,
            accion AS action
        FROM raw_calificadores
    """
    df = pd.read_sql(query, pg_engine)
    df.to_sql("fact_ratings", ch_engine, if_exists="append", index=False)
    print(f"Loaded fact_ratings: {len(df)} rows")

def has_new_data():
    current_count_query = "SELECT COUNT(*) AS total FROM raw_precios_diarios"
    control_query = "SELECT last_row_count FROM etl_control WHERE process_name = 'load_clickhouse'"

    current_count = pd.read_sql(current_count_query, pg_engine).iloc[0]["total"]
    control_df = pd.read_sql(control_query, pg_engine)

    if control_df.empty:
        print("No previous control record found. Initial load will run.")
        return True, current_count

    last_count = control_df.iloc[0]["last_row_count"]

    if current_count != last_count:
        print(f"New data detected in landing zone. Previous count: {last_count}, current count: {current_count}")
        return True, current_count

    print("No new data detected in landing zone. ClickHouse load will be skipped.")
    return False, current_count

def update_control_table(current_count):
    upsert_sql = f"""
        INSERT INTO etl_control (process_name, last_row_count, last_execution_ts)
        VALUES ('load_clickhouse', {current_count}, CURRENT_TIMESTAMP)
        ON CONFLICT (process_name)
        DO UPDATE SET
            last_row_count = EXCLUDED.last_row_count,
            last_execution_ts = EXCLUDED.last_execution_ts;
    """

    with pg_engine.begin() as conn:
        conn.execute(text(upsert_sql))

    print("Control table updated successfully.")

if __name__ == "__main__":
    should_run, current_count = has_new_data()

    if not should_run:
        print("Process finished without loading ClickHouse.")
    else:
        with ch_engine.begin() as conn:
            conn.execute(text("TRUNCATE TABLE gobierno_datos_olap.dim_bank_info"))
            conn.execute(text("TRUNCATE TABLE gobierno_datos_olap.fact_daily_prices"))
            conn.execute(text("TRUNCATE TABLE gobierno_datos_olap.fact_fundamentals"))
            conn.execute(text("TRUNCATE TABLE gobierno_datos_olap.fact_holders"))
            conn.execute(text("TRUNCATE TABLE gobierno_datos_olap.fact_ratings"))
            conn.execute(text("TRUNCATE TABLE gobierno_datos_olap.monthly_stock_summary"))

        load_dim_bank_info()
        load_fact_daily_prices()
        load_fact_fundamentals()
        load_fact_holders()
        load_fact_ratings()

        with ch_engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO gobierno_datos_olap.monthly_stock_summary
                (
                    ticker,
                    year,
                    month,
                    avg_open_price,
                    avg_close_price,
                    avg_volume
                )
                SELECT
                    ticker,
                    toYear(trade_date) AS year,
                    toMonth(trade_date) AS month,
                    avg(open_price) AS avg_open_price,
                    avg(close_price) AS avg_close_price,
                    avg(volume) AS avg_volume
                FROM gobierno_datos_olap.fact_daily_prices
                GROUP BY
                    ticker,
                    toYear(trade_date),
                    toMonth(trade_date)
            """))

        update_control_table(current_count)
        print("ClickHouse load completed successfully.")