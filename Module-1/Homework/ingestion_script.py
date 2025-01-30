import time
import argparse
import os
import pandas as pd
from sqlalchemy import create_engine

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = int(params.port)
    db = params.db
    table_name = params.table_name
    url = params.url
    file_name = params.file_name
    chunk_size = 100000  

    print(f"Downloading file: {file_name}")
    exit_code = os.system(f"wget {url} -O {file_name}")

    print(f"{file_name} downloaded successfully.")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    with engine.connect() as connection:
        print("Connection successful!")

    df = pd.read_csv(file_name, chunksize=chunk_size)


    print("CSV file read successfully.")

    first_chunk = next(df)

    dt_exist = 0
    if 'lpep_pickup_datetime' in first_chunk.columns and 'lpep_dropoff_datetime' in first_chunk.columns:
        dt_exist = 1
        first_chunk['lpep_pickup_datetime'] = pd.to_datetime(first_chunk['lpep_pickup_datetime'], errors='coerce')
        first_chunk['lpep_dropoff_datetime'] = pd.to_datetime(first_chunk['lpep_dropoff_datetime'], errors='coerce')
        print("Datetime columns converted.")
    else:
        print("No Datetime columns found.")

    first_chunk.head(0).to_sql(name=table_name, con=engine, if_exists="replace", index=False)

    first_chunk.to_sql(name=table_name, con=engine, if_exists="append", index=False)
    print("First chunk inserted into the table.")

    while True:
        t_start = time.time()

        try:
            chunk = next(df)
        except StopIteration:
            print("Insertion is complete.")
            break

        # If datetime columns exist, convert them in the current chunk
        if dt_exist:
            chunk['lpep_pickup_datetime'] = pd.to_datetime(chunk['lpep_pickup_datetime'], errors='coerce')
            chunk['lpep_dropoff_datetime'] = pd.to_datetime(chunk['lpep_dropoff_datetime'], errors='coerce')

        chunk.to_sql(name=table_name, con=engine, if_exists="append", index=False)

        t_end = time.time()
        print(f'Inserted another chunk... took {t_end - t_start:.3f} second(s)')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")
    parser.add_argument('--user', help="user name for postgres")
    parser.add_argument('--password', help="password for postgres")
    parser.add_argument('--host', help="host for postgres")
    parser.add_argument('--port', help="port for postgres")
    parser.add_argument('--db', help="database name for postgres")
    parser.add_argument('--table_name', help="table name to write the data into")
    parser.add_argument('--url', help="url for the csv")
    parser.add_argument('--file_name', help="file name")

    args = parser.parse_args()

    main(args)