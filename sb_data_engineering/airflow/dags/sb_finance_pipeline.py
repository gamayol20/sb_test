from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="sb_finance_pipeline",
    start_date=datetime(2026, 4, 13),
    schedule="@daily",
    catchup=False,
    tags=["sb", "finance", "data_engineering"],
) as dag:

    extract_basic_info = BashOperator(
        task_id="extract_basic_info",
        bash_command='python3 /opt/airflow/project/app/extract/extract_basic_info_multi.py'
    )

    extract_prices = BashOperator(
        task_id="extract_prices",
        bash_command='python3 /opt/airflow/project/app/extract/extract_prices_multi.py'
    )

    extract_fundamentals = BashOperator(
        task_id="extract_fundamentals",
        bash_command='python3 /opt/airflow/project/app/extract/extract_fundamentals_multi.py'
    )

    extract_holders = BashOperator(
        task_id="extract_holders",
        bash_command='python3 /opt/airflow/project/app/extract/extract_holders_multi.py'
    )

    extract_ratings = BashOperator(
        task_id="extract_ratings",
        bash_command='python3 /opt/airflow/project/app/extract/extract_ratings_multi.py'
    )

    load_postgres = BashOperator(
        task_id="load_postgres",
        env={"POSTGRES_HOST": "postgres"},
        bash_command='python3 /opt/airflow/project/app/load/load_landing_postgres.py'
    )

    load_clickhouse = BashOperator(
        task_id="load_clickhouse",
        env={"POSTGRES_HOST": "postgres", "CLICKHOUSE_HOST": "clickhouse"},
        bash_command='python3 /opt/airflow/project/app/load/load_clickhouse.py'
    )

    [extract_basic_info, extract_prices, extract_fundamentals, extract_holders, extract_ratings] >> load_postgres >> load_clickhouse