def ingest_dataframe(df, table_name, engine):
    if df.empty:
        print("No data found !!")
        return

    # If timestamp is the index → move it into a column explicitly
    if df.index.name:
        df = df.reset_index().rename(columns={df.index.name: "timestamp"})
    else:
        # If already a column, ensure correct name
        if "timestamp" not in df.columns:
            df = df.rename(columns={df.columns[0]: "timestamp"})
        if "index" in df.columns and not "timestamp" in df.columns:
            df = df.rename(columns={"index": "timestamp"})
    # Rename Alpha Vantage columns for consistency
    rename_map = {
        "1. open": "open",
        "2. high": "high",
        "3. low": "low",
        "4. close": "close",
        "5. volume": "volume"
    }
    df = df.rename(columns=rename_map)

    # Insert into Postgres
    df.to_sql(
        table_name,
        engine,
        if_exists="append",   # append only
        index=False,          # don't insert DataFrame index
        method="multi"
    )

    print(f"Inserted {len(df)} rows into {table_name}")


    

