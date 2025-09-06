def ingest_dataframe(df, table_name, engine):
    if df.empty:
        print("No data found !!")
        return

    # Ensure timestamp is a normal column, not an index
    df = df.reset_index()

    # Insert only, never recreate the table

    df.to_sql(
        table_name,
        engine,
        if_exists="append",   # creates table if not exists
        index=False,
        method="multi"
    )

    print(f"Inserted {len(df)} rows into {table_name}")
