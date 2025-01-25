import os
import time
import argparse 
import urllib.parse
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
    csv_name = 'yellow_taxi_data.csv'
    file_name = os.path.basename(urllib.parse.urlparse(url).path)

    # Download the file
    print(f"Downloading file: {file_name}")
    os.system(f"wget {url} -O {file_name}")  # Use -O to specify the output file name

    # Read the downloaded file
    if file_name.endswith('.parquet'):
        df = pd.read_parquet(file_name)
    elif file_name.endswith('.csv'):
        df = pd.read_csv(file_name)
    else:
        raise ValueError(f"Unsupported file format: {file_name}")

    # Save the DataFrame as a CSV file
    csv_name = 'yellow_taxi_data.csv'
    df.to_csv(csv_name, index=False)

    print(f"File saved as: {csv_name}")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    with engine.connect() as connection:
        print("Connection successful!")

    pd.io.sql.get_schema(df, name=table_name)

    df_structure = df.head(0)

    df_structure.to_sql(name=table_name, con=engine, if_exists="replace")

    i = 0
    chunk_size = 10000

    while i < len(df):
        t_start = time.time()

        df[i:i + chunk_size].to_sql(
            name=table_name, 
            con=engine, 
            if_exists="append"
        )

        i += chunk_size
        t_end = time.time()

        print('Inserted another chunk... took %.3f second(s)' % (t_end - t_start))

    print("Insertion is compelete")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Ingest CSV data to Postgres")

    parser.add_argument('--user', help="user name for postgres")
    parser.add_argument('--password', help="password for postgres")
    parser.add_argument('--host', help="host for postgres")
    parser.add_argument('--port', help="port for postgres")
    parser.add_argument('--db', help="database name for postgres")
    parser.add_argument('--table_name', help="name of the table where we will write the results to")
    parser.add_argument('--url', help="url of the CSV")

    args = parser.parse_args()

    main(args)
