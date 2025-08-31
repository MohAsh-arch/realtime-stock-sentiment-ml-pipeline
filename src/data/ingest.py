def ingest_dataframe(df, table_name, engine):
    if df.empty:
        print("No data found !!")
        return
    df.to_sql(table_name, engine, if_exists="append", index=True, index_label = "timestamp" )
    print(f"Inserted {len(df)} into {table_name}")