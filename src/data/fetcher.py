import fetch
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
url = 'https://www.alphavantage.co/query?'

client = fetch.AlphaVantageClient(api_key,url)

df_intraday = client.fetch_intraday('AAPL')

client.save_to_csv(df_intraday,'appl_interaday')

df_daily = client.fetch_daily("AAPL")
client.save_to_csv(df_daily, "aapl_daily")

print(df_intraday.head())
