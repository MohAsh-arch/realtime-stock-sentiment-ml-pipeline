import requests
import pandas as pd
from utilities.logger import logger

class AlphaVantageClient:
    def __init__(self, api_key, base_url="https://www.alphavantage.co/query"):
        self.api_key = api_key
        self.base_url = base_url

    def _fetch(self, function, symbol, **kwargs):
        """Generic fetcher for any Alpha Vantage time series function"""
        params = {
            "function": function,
            "symbol": symbol,
            "apikey": self.api_key,
            **kwargs
        }
        logger.info(f"Fetching {function} for {symbol} with params={kwargs}")

        r = requests.get(self.base_url, params=params, timeout=10)
        data = r.json()

        # --- Error handling ---
        if "Error Message" in data:
            logger.error(f"Invalid request for {symbol}: {data['Error Message']}")
            raise ValueError(f"Invalid request: {data['Error Message']}")

        if "Note" in data:  
            logger.warning(f"API limit reached while fetching {symbol}")
            raise RuntimeError("API limit reached. Try again later.")

        # --- Extract time series dynamically ---
        ts_key = next((k for k in data.keys() if "Time Series" in k), None)
        if not ts_key:
            logger.error(f"Unexpected API response for {symbol}, no time series found.")
            raise ValueError("Unexpected API response, no time series found.")

        ts_data = data[ts_key]

        # --- Convert to DataFrame ---
        df = pd.DataFrame.from_dict(ts_data, orient="index")
        df.index = pd.to_datetime(df.index)  
        df = df.rename(columns={
            "1. open": "open",
            "2. high": "high",
            "3. low": "low",
            "4. close": "close",
            "5. volume": "volume"
        })
        df = df.astype(float)  
        df = df.sort_index()   

        logger.info(f"Received {len(ts_data)} rows for {symbol}")
        logger.debug(f"Data sample:\n{df.head()}")

        return df

    def fetch_intraday(self, symbol, interval="5min"):
        """Fetch intraday time series data for a given symbol and interval."""
        return self._fetch("TIME_SERIES_INTRADAY", symbol, interval=interval)

    def fetch_daily(self, symbol):
        """Fetch daily time series data for a given symbol."""
        return self._fetch("TIME_SERIES_DAILY", symbol)

    def save_to_csv(self, df, file_name):
        """Save a DataFrame to CSV with logging."""
        path = f"{file_name}.csv"
        df.to_csv(path, index=True)
        logger.info(f"Saved data to {path}")
