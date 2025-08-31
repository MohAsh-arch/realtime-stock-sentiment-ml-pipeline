from src.data import fetch
import os
from dotenv import load_dotenv
from src.db import connection
from src.data.ingest import ingest_dataframe
from src.db.connection import engine
load_dotenv()



api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
url = 'https://www.alphavantage.co/query?'

client = fetch.AlphaVantageClient(api_key,url)

df_intraday = client.fetch_intraday('AAPL')
#
ingest_dataframe(df_intraday, "stock_intraday" , engine)

