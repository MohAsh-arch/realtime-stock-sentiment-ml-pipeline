from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import os, sys

SRC_PATH = os.path.join(os.path.dirname(__file__), "..", "src")
SRC_PATH = os.path.abspath(SRC_PATH)
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

from src.data.fetcher import fetch_stock_data





with DAG(
    dag_id="stock_etl_pipeline",
    start_date=days_ago(1),
    schedule_interval="*/5 * * * *",  # every 5 mins
    catchup=False,
    tags=["stocks", "etl"],
) as dag:

    etl_task = PythonOperator(
        task_id="run_stock_etl",
        python_callable=fetch_stock_data,
        op_kwargs={"symbol": "AAPL"},
    )
