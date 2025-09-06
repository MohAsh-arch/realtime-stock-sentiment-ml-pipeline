from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os, sys
import pandas as pd
from dotenv import load_dotenv

# Make sure src is in the path
SRC_PATH = os.path.join(os.path.dirname(__file__), "..", "src")
SRC_PATH = os.path.abspath(SRC_PATH)
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)

# Import project modules
from src.db.connection import engine
from src.data import fetch
from src.data.data_cleaner import clean_stock_data
from src.data.ingest import ingest_dataframe

# Load env vars
load_dotenv()
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
url = "https://www.alphavantage.co/query?"
client = fetch.AlphaVantageClient(api_key, url)

# Companies to track
symbols = ["AAPL", "MSFT", "GOOGL"]

# ------------------- PIPELINE FUNCTIONS -------------------

def fetch_to_db(symbol):
    raw = client.fetch_intraday(symbol)       # fetch intraday
    raw["symbol"] = symbol                    # add symbol column
    ingest_dataframe(raw, "raw_stock_data", engine)   # insert raw into Postgres

def clean_to_db(symbol):
    raw = pd.read_sql(f"SELECT * FROM raw_stock_data WHERE symbol='{symbol}'", engine)
    cleaned = clean_stock_data(raw, symbol)   # clean raw data
    ingest_dataframe(cleaned, "cleaned_stock_data", engine)

def final_ingest(symbol):
    cleaned = pd.read_sql(f"SELECT * FROM cleaned_stock_data WHERE symbol='{symbol}'", engine)
    ingest_dataframe(cleaned, "stock_data", engine)   # final table

# ------------------- DAG DEFINITION -------------------

with DAG(
    "stock_pipeline_intraday",
    start_date=datetime(2025, 9, 6),
    schedule_interval="*/5 * * * *",  # every 5 minutes
    catchup=False,
) as dag:

    for symbol in symbols:
        fetch_task = PythonOperator(
            task_id=f"fetch_{symbol}",
            python_callable=fetch_to_db,
            op_args=[symbol],
        )

        clean_task = PythonOperator(
            task_id=f"clean_{symbol}",
            python_callable=clean_to_db,
            op_args=[symbol],
        )

        ingest_task = PythonOperator(
            task_id=f"ingest_{symbol}",
            python_callable=final_ingest,
            op_args=[symbol],
        )

        fetch_task >> clean_task >> ingest_task
