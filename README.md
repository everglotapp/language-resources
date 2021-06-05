# language-resources
This repo stores language related resources. Files are stores under the `resources` folder in the form of 'records' formatted JSON (Pandas dataframe orient)

## Load json file to postgres database
To install depencies, run
```
pip3 install -r requirements.txt
```
To load a json file into the postgres database, run
```
python3 ./scripts/json_to_postgres.py --path ./resources/file_name.json
```
This will load the data in `./resources/file_name.json` into table `app_public.file_name` by default.
To specify the table use the `--table` argument.
To specify postgres url use the `--postgres` argument, by default it uses `postgresql+psycopg2://everglot_app_user@127.0.0.1:5433/everglot_app_db`. Make sure the DB is forwarded to the right port before running the script.