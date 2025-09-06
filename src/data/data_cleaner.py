import pandas as pd
import logging

logger = logging.getLogger(__name__)

def data_cleaner(raw_data: dict, symbol: str) -> pd.DataFrame:
    """
    Convert raw AlphaVantage JSON response into a clean DataFrame.
    """
    # Find the time series key
    ts_key = next((k for k in raw_data.keys() if "Time Series" in k), None)
    if not ts_key:
        logger.error(f"No time series found in response for {symbol}")
        return pd.DataFrame()

    ts_data = raw_data[ts_key]

    # Convert to DataFrame
    df = pd.DataFrame.from_dict(ts_data, orient="index")
    df.index = pd.to_datetime(df.index, errors="coerce")

    # Rename columns
    df = df.rename(columns={
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. volume": "volume"
    })

    # Converting numeric columns safely
    numeric_cols = ["open", "high", "low", "close", "volume"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # Droping rows with missing values
    df = df.dropna()

    # Add symbol column
    df["symbol"] = symbol

    # Sort by time
    df = df.sort_index()

    logger.info(f"Cleaned {len(df)} rows for {symbol}")
    return df
