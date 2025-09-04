import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from src.data.fetcher import fetch_stock_data


with DAG(
    dag_id="fetch_stock_data",
    description="Fetch stock prices and insert into Postgres",
    start_date=days_ago(1),
    schedule_interval="*/5 * * * *",  
    catchup=False,
    tags=["stocks", "etl"]
) as dag:

    fetch_task = PythonOperator(
        task_id="fetch_task",
        python_callable=fetch_stock_data
    )

    fetch_task
