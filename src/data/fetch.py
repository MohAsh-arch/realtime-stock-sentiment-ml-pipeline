import requests
import pandas as pd

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
        r = requests.get(self.base_url, params=params)
        data = r.json()


        # --- Error handling ---
        if "Error Message" in data:
            raise ValueError(f"Invalid request: {data['Error Message']}")
        if "Note" in data:  
            raise RuntimeError("API limit reached. Try again later.")
        
        # --- Extract time series dynamically ---
        ts_key = next((k for k in data.keys() if "Time Series" in k), None)
        if not ts_key:
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
        df = df.astype(float)  # convert all columns to numeric
        df = df.sort_index()   # ascending order
        return df

    def fetch_intraday(self, symbol, interval="5min"):
        return self._fetch("TIME_SERIES_INTRADAY", symbol, interval=interval)

    def fetch_daily(self, symbol):
        return self._fetch("TIME_SERIES_DAILY", symbol)

    def save_to_csv(self, df, file_name):
        df.to_csv(f"{file_name}.csv", index=True)
