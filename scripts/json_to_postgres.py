import os
import csv
from io import StringIO
from sqlalchemy import create_engine
import pandas as pd
import uuid
import argparse
from pathlib import Path
from os import listdir


parser = argparse.ArgumentParser()
parser.add_argument("--path", type=str,
                    help="Path to json file"
                    )
parser.add_argument("--table", type=str,
                    help="Table name to load, default app_public.json_file_name")
parser.add_argument("--postgres", type=str,
                    help="postgres Url")
args = parser.parse_args()

path = Path(args.path)
file_base = os.path.basename(path)
filename = os.path.splitext(file_base)[0]

if args.table:
    TABLE_NAME = args.table
else:
    TABLE_NAME = "app_public." + filename

if args.postgres:
    POSTGRES_URL = args.postgres
else:
    POSTGRES_URL = 'postgresql+psycopg2://everglot_app_user@127.0.0.1:5433/everglot_app_db'

def psql_insert_copy(table, conn, keys, data_iter):
    dbapi_conn = conn.connection
    with dbapi_conn.cursor() as cur:
        s_buf = StringIO()
        writer = csv.writer(s_buf)
        writer.writerows(data_iter)
        s_buf.seek(0)

        columns = ', '.join('"{}"'.format(k) for k in keys)
        if table.schema:
            table_name = '{}.{}'.format(table.schema, table.name)
        else:
            table_name = table.name

        sql = 'COPY {} ({}) FROM STDIN WITH CSV'.format(
            table_name, columns)
        cur.copy_expert(sql=sql, file=s_buf)


def load_df_to_table(df, table_name, postgres_url):
    engine = create_engine(postgres_url)
    df.to_sql(table_name, engine, method=psql_insert_copy, if_exists='append', index=False)


def json_to_table(filename):

    df = pd.read_json(filename, orient='records')
    
    # Set uuid for each row    
    df['uuid'] = [uuid.uuid4() for _ in range(len(df.index))]

    # If column type in postgres is array, change the column to a set
    for col in df.columns:
        if type(df[col][0]) is list:
            df[col] = df[col].apply(set)

    load_df_to_table(df, TABLE_NAME, POSTGRES_URL)


if __name__ == "__main__":
    if args.path:
        json_to_table(args.path)
    else:
        for file in listdir('./resources'):
            try:
                json_to_table(file)
            except:
                print(f"Failed to load {file}")

