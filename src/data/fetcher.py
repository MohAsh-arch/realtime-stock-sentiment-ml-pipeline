from src.data import fetch
import os
from dotenv import load_dotenv
from src.db import connection
from src.data.ingest import ingest_dataframe
from src.db.connection import engine
load_dotenv()
from src.data.data_cleaner import data_cleaner


def fetch_stock_data():
    api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
    url = 'https://www.alphavantage.co/query?'

    client = fetch.AlphaVantageClient(api_key,url)

    tickers = [
    # Big Tech / FAANG
    "AAPL", "MSFT", "GOOGL", "AMZN", "META",
    
    # Finance
    "JPM", "BAC", "GS",
    
    # Energy
    "XOM", "CVX",
    
    # Consumer / Retail
    "WMT", "KO",
    
    # Emerging / High Volatility
    "TSLA", "NVDA",
    
    # ETFs / Indices
    "SPY", "QQQ"
]

    for ticket in tickers:
        raw_intraday = client.fetch_intraday(ticket)
        df_cleanded = data_cleaner(raw_intraday, ticket)
        ingest_dataframe(df_cleanded, 'stock_data', engine)


