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
        if_exists="append",   # append only
        index=False,          # don't use pandas index
        method="multi"        # faster batch insert
    )

    print(f"Inserted {len(df)} rows into {table_name}")
